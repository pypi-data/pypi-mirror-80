"""Declares :class:`GenericOAuth2Provider`."""
from .base import BaseOAuth2Provider


class GenericOAuth2Provider(BaseOAuth2Provider):
    """Generic OAuth2 provider implementation."""

    def get_asserted_subject_id(self, cs): # pylint: disable=invalid-name
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        raise NotImplementedError("Subclasses must override this method.")
