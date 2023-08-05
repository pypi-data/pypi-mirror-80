# pylint: disable=W0223,W0231
"""Declares :class:`StaticPasswordProvider`."""
import base64
import os

import ioc
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.crypto import constant_time_compare

from .provider import BaseProvider


class StaticPasswordProvider(BaseProvider):
    """An identity provider that has a static username/password
    combination.
    """

    @classmethod
    def fromenv(cls, env):
        """Create a new :class:`StaticPasswordProvider` from environment
        variables.
        """
        return cls(env['DEBUG_USERNAME'], env['DEBUG_PASSWORD'])

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = 'static'
        self.description = "Debug"

    @ioc.inject('subjects', 'iam.SubjectRepository')
    @ioc.inject('factory', 'iam.SubjectFactory')
    def check_password(self, username, password, subjects, factory):
        """Check if username/password is a valid combination and return a
        :class:`iam.ext.idc.models.AssertedSubject` or ``None``.
        """
        if not constant_time_compare(username, self.username)\
        or not constant_time_compare(password, self.password):
            return None
        try:
            sub = subjects.get(asid=username)
        except subjects.DoesNotExist:
            sub = factory.new()
        sub.asid = username
        sub.external = False
        sub.is_superuser = os.getenv('DEBUG_SUPERUSER') == '1'
        subjects.persist(sub)
        return sub

    def is_default(self):
        """Return a boolean indicating if the provider has marked itself as
        a default provider.
        """
        return None

    def start_authentication(self, request, _, next_url, **kwargs): # pylint: disable=W0613
        """Prompt the client for credentials."""
        if request.user.is_authenticated:
            return HttpResponseRedirect(next_url)

        subject = self._parse_auth_header(request)
        if not subject:
            response = HttpResponse(status=401)
            response['WWW-Authenticate'] = 'Basic'
        else:
            self.login(request, subject)
            response = HttpResponseRedirect(next_url)
        return response

    def _parse_auth_header(self, request):
        try:
            _, data = str.split(request.META['HTTP_AUTHORIZATION'], ' ')
            username, password = str.split(bytes.decode(base64.b64decode(data)), ':')
            return self.authenticate(request, username=username,
                password=password, provider=self)
        except (ValueError, KeyError):
            return None
