"""Declares :class:`AuthenticationCtrl`."""
import functools
import logging
import time
import uuid

import ioc
from django.core.signing import BadSignature
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.middleware.csrf import rotate_token
from django.urls import include
from django.urls import reverse
from django.urls import path
from django.utils.decorators import method_decorator
from django.utils.http import  url_has_allowed_host_and_scheme
from django.views.decorators.csrf import ensure_csrf_cookie

from iam.ext.idc.lib import IdentityProvidersRegistry


class AuthenticationCtrl:
    """A controller that manages the authentication flow using the SAML2
    or OAuth2 protocols.
    """
    logger = logging.getLogger('iam.audit')
    redirect_cookie_name = 'idc.post_login_redirect'
    success_url_allowed_hosts = set()

    @property
    def urlpatterns(self):
        """Return the list of URL patterns exposed by :class:`AuthenticationCtrl`."""
        return [
            path('login', self.login_using_default,
                name='login.default'),
            path('error', self.nologin,
                name='nologin'),
            path('providers/default', self.get_default_provider,
                name='providers.default'),
            path('providers', self.list_providers, name='providers'),
            path('<str:using>/authorize', self.inject_provider(self.authorize),
                name='authorize'),
            path('<str:using>/login', self.inject_provider(self.login),
                name='login'),
        ]

    @classmethod
    def as_namespace(cls, base_path, namespace='iam', registry=None):
        """Instantiate a :class:`AuthenticationCtrl` instance and return an
        iterable suitable for use with :func:`django.urls.include`.

        Args:
            base_path (str): the base path to mount the URLs to. Must not
                include a leading slash.
            namespace (str): the URL namespace. Defaults to ``iam``.
            registry: a :class:`IdentityProvidersRegistry` instance. May
                be ``None``, in which case the default registry is used.

        Returns:
            iterable
        """
        ctrl = cls(registry or IdentityProvidersRegistry(
            ioc.require('iam.IdentityProviderLoaders')), namespace=namespace)
        return path(base_path, include((ctrl.urlpatterns, 'idc'), namespace=namespace))

    def __init__(self, registry, namespace):
        self.registry = registry
        self.namespace = namespace

    def authorize(self, request, provider):
        """Invoked when the user is redirected by the OAuth2 SSO provider after the
        authentication dialog.
        """
        try:
            subject = provider.get_asserted_subject(request)
        except Exception as e: # pylint: disable=W0703,C0103
            self.logger.error("Invalid response from provider '%s': %s",
                provider.name, e.args[0])
            return HttpResponse(status=500)
        if subject is not None:
            provider.login(request, subject)
            redirect_to = self.get_login_redirect(request)
        else:
            redirect_to = reverse('iam:nologin')
        response = HttpResponseRedirect(redirect_to)
        response.delete_cookie(self.redirect_cookie_name)
        return response

    def inject_provider(self, func):
        """Decorate `func` so that the provider is injected based on the
        `using` URL parameter.
        """
        @functools.wraps(func)
        def f(request, using, *args, **kwargs): # pylint: disable=C0103
            try:
                return func(request, self.registry.get(using), *args, **kwargs)
            except KeyError:
                list_url = self.get_enabled_providers_uri(request)
                dto = {
                    'id': str(uuid.uuid4()),
                    'timestamp': int(time.time() * 1000),
                    'code': "IDENTITY_PROVIDER_DOES_NOT_EXIST",
                    'message': f"The selected identity provider '{using}' does not exist.",
                    'hint': f"Inspect {list_url} for a list of enabled identity providers.",
                    'audit': {
                        'message': "This error is recorded along with your IP address."
                    }
                }
                self.logger.info(
                    "Unknown provider '%s' requested from host %s (id: %s)",
                    using, 'n.o.o.p', dto['id'])
                return JsonResponse(dto, status=404,
                    json_dumps_params={'indent': 2})

        return f

    def get_authorize_uri(self, request, using): # pylint: disable=unused-argument
        """Return the absolute URL to which the :term:`Asserting Party` must
        redirect after the login dialog.
        """
        return request.build_absolute_uri(
            reverse(f'{self.namespace}:authorize', kwargs={'using': using}))

    def get_default_provider(self, request):
        """Return a JSON response containing the default OAuth2 provider."""
        provider = self.registry.get_default_provider()
        return JsonResponse({
            'description': provider.description,
            'name': provider.name,
            'loginUrl': self.get_login_uri(request, provider.name)
            }, json_dumps_params={'indent': 2})

    def get_enabled_providers_uri(self, request):
        """Return URL yielding the enabled providers."""
        return request.build_absolute_uri(reverse(f'{self.namespace}:providers'))

    def get_login_uri(self, request, using):
        """Return the login URL for the given provider."""
        return request.build_absolute_uri(
            reverse(f'{self.namespace}:login', kwargs={'using': using}))

    def get_login_redirect(self, request):
        """Inspect the cookies on the request object and return the URL to
        which the client must redirect after a succesful authentication. Also
        inspect the ``?next`` parameter, since there may be cookies left over
        from a failed authentication attempt.
        """
        try:
            redirect_to = request.get_signed_cookie(self.redirect_cookie_name)\
                if 'next' not in request.GET\
                else request.GET['next']
        except (LookupError, BadSignature):
            redirect_to = '/'
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(request),
            require_https=request.is_secure(),
        )
        return redirect_to if url_is_safe else '/'

    def get_success_url_allowed_hosts(self, request):
        """Return the set of allowed hosts to redirect to."""
        return {request.get_host(), *self.success_url_allowed_hosts}

    def list_providers(self, request):
        """Return a JSON response containing the enabled OAuth2 providers."""
        rotate_token(request)
        return JsonResponse({
            'providers': [{
            'description': x.description,
            'loginUrl': self.get_login_uri(request, x.name)
        } for x in self.registry.enabled()]}, json_dumps_params={'indent': 2})

    @method_decorator(ensure_csrf_cookie)
    def login(self, request, provider):
        """Redirect the client to the identity provider login screen."""
        if provider is None:
            return HttpResponse("The server did not configure any identity providers.",
                status=503)
        redirect_to = self.get_login_redirect(request) or '/'
        response = provider.start_authentication(request,
            self.get_authorize_uri(request, provider.name),
            next_url=redirect_to)
        response.set_signed_cookie(self.redirect_cookie_name, redirect_to,
            max_age=60, httponly=True)
        return response

    def login_using_default(self, request):
        """Login using the default provider."""
        return self.login(request, self.registry.get_default_provider())

    def nologin(self, request): # pylint: disable=W0613,R0201
        """Display an error message when we refuse to authenticate the user."""
        return HttpResponse("Unable to authenticate.", status=403)
