"""Declares :class:`OIDCGenericProvider`."""
from .base import BaseOAuth2Provider


class OIDCGenericProvider(BaseOAuth2Provider):
    """Generic implementation of OAuth2 using the OpenID Connect (OIDC)
    protocol.
    """

    def get_asserted_subject_id(self, cs): # pylint: disable=invalid-name
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        raise NotImplementedError("Subclasses must override this method.")
