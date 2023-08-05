# pylint: disable=invalid-name
"""Declares :class:`BaseOAuth2Provider`."""
import ioc

from iam.canon.idc import OAuth2ProviderSpecSchema
from ...provider import BaseProvider


class BaseOAuth2Provider(BaseProvider):
    """The base class for all OAuth2 providers."""
    schema = OAuth2ProviderSpecSchema()
    metadata_url = None

    @property
    def name(self):
        """Return the name with which the client was registered in the
        :mod:`authlib` library.
        """
        return self._client.name

    @property
    def description(self):
        """Return the description as specified in the resource."""
        return self._spec['description']

    @classmethod
    def fromresource(cls, resource, oauth, *args, **kwargs): # pylint: disable=arguments-differ
        """Create a new :class:`OIDCGenericProvider` from a provider
        resource.
        """
        meta = resource['metadata']
        spec = cls.schema.load(resource['spec'])
        credentials = spec.pop('credentials')
        client = cls.get_client(oauth, meta, spec, credentials,
            url=getattr(cls, 'metadata_url', None),
            client_kwargs=cls.get_client_kwargs(spec))
        return cls.fromclient(client, spec)

    @staticmethod
    def get_client(oauth, meta, spec, credentials, url=None, client_kwargs=None): # pylint: disable=R0913
        """Create an OAuth2 client using the provided parameters."""
        url = url or spec.get('url')
        kwargs = {
            'name': meta['name'],
            'client_id': credentials['id'],
            'client_secret': credentials['secret'],
            'client_kwargs': client_kwargs
        }
        if url:
            kwargs['server_metadata_url'] = url
        elif spec.get('metadata'):
            kwargs.update({
                'request_token_url': spec['metadata']['request_token']['url'],
                'request_token_params': spec['metadata']['request_token']['params'],
                'access_token_url': spec['metadata']['access_token']['url'],
                'access_token_params': spec['metadata']['access_token']['params'],
                'base_url': spec['metadata']['base_url'],
                'authorize_url': spec['metadata']['authorize_url']
            })
        else:
            raise ValueError("Specify either providerMetadata or metadataUrl")
        return oauth.register(**kwargs)

    @staticmethod
    def get_client_kwargs(*args, **kwargs): # pylint: disable=unused-argument
        """Return the client keyword arguments for the specified
        provider `spec`.
        """
        return None

    @classmethod
    def fromclient(cls, client, spec):
        """Return a new :class:`BaseOAuth2Provider` from a :mod:`authlib`
        OAuth2 client object.
        """
        return cls(client, spec)

    def __init__(self, client, spec, *args, **kwargs):
        super().__init__(spec, *args, **kwargs)
        self._client = client

    def authorize_redirect(self, request, redirect_to, **kwargs):
        """Initiate the OAuth2 login dialog by redirecting the user to the
        SSO provider login screen.
        """
        return self._client.authorize_redirect(request, redirect_to, **kwargs)

    start_authentication = authorize_redirect

    def get_asserted_subject(self, request):
        """Invoked after the OAuth2 provider redirects the client upon
        succesfully completing the authentication dialog.
        """
        return self.authenticate(
            request,
            token=self._client.authorize_access_token(request),
            provider=self
        )

    def get_asserted_subject_id(self, cs): # pylint: disable=invalid-name
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        raise NotImplementedError("Subclasses must override this method.")

    @ioc.inject('subjects', 'iam.SubjectRepository')
    @ioc.inject('factory', 'iam.SubjectFactory')
    def token_to_subject(self, request, token, subjects, factory):
        """Exchange an access token for an OIDC ID token, and get or
        create a corresponding :term:`Subject` from the persistent
        data store.
        """
        cs = self._client.parse_id_token(request, token)
        asid = self.get_asserted_subject_id(cs)
        try:
            sub = subjects.get(asid=asid)
        except subjects.DoesNotExist:
            sub = factory.new()
        sub.asid = asid
        sub.external = bool(self._spec.get('external'))
        sub.is_superuser = self.is_superuser(cs)
        subjects.persist(sub)
        return sub

    def is_superuser(self, cs):
        """Return a boolean indicating if the :term:`Subject` asserted by
        the claims set is a superuser.
        """
        if bool(self._spec.get('is_superuser')):
            return True
        yes = False
        for superuser in (self._spec.get('superusers') or []):
            claim, value = str.split(superuser, ':')
            if cs.get(claim) != value:
                continue
            yes = True
            break
        return yes
