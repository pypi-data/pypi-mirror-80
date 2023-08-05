"""Declares :class:`GoogleOIDCProvider`."""
import ioc

from .oidc import OIDCGenericProvider


class GoogleOIDCProvider(OIDCGenericProvider):
    """Implements OAuth2 with Google using OpenID Connect (OIDC)."""
    metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
    default_scope = ["openid", "email", "profile"]

    @classmethod
    def fromenv(cls, env):
        """Instantiate a new :class:`GoogleOIDCProvider` from environment
        variables.
        """
        oauth = ioc.require('OAuth2Registry')
        client = oauth.register(
            name='google-oidc',
            client_id=env['GOOGLE_OAUTH_CLIENT_ID'],
            client_secret=env['GOOGLE_OAUTH_CLIENT_SECRET'],
            client_kwargs={
                'scope': env['GOOGLE_OAUTH_SCOPE']
                    if 'GOOGLE_OAUTH_SCOPE' in env\
                    else str.join(' ', cls.default_scope)
            },
            server_metadata_url=cls.metadata_url
        )
        return cls(client, {'description': "Google"})

    @staticmethod
    def get_client_kwargs(spec): # pylint: disable=arguments-differ
        """Return the client keyword arguments for the specified
        provider `spec`.
        """
        kwargs = {}
        if spec.get('scope'):
            kwargs['scope'] = str.join(' ', spec['scope'])
        return kwargs

    def get_asserted_subject_id(self, cs):
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        return f"{cs['sub']}@{cs['aud']}"
