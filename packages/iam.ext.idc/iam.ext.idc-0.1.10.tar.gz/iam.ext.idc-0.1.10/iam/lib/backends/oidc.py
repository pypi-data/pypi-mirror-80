# pylint: disable=arguments-differ
"""Declares :class:`OIDCAuthenticationBackend`."""
import ioc

from django.contrib.auth.backends import BaseBackend


class OIDCAuthenticationBackend(BaseBackend):
    """Implements Django authentication for OAuth2 providers using
    OpenID Connect.
    """

    def authenticate(self, request, token=None, provider=None):  # pragma: no cover
        """Use `token` to receive a claims set from the OIDC provider
        `provider`.
        """
        return provider.token_to_subject(request, token)

    @ioc.inject('subjects', 'iam.SubjectRepository') # pragma: no cover
    def get_user(self, lsid, subjects):
        """Return the :term:`Subject` identified by `lsid`."""
        return subjects.get(pk=lsid)
