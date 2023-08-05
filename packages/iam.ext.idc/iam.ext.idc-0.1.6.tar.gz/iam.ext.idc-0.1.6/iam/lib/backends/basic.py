# pylint: disable=arguments-differ
"""Declares :class:`BasicAuthenticationBackend`."""
import ioc

from django.contrib.auth.backends import BaseBackend


class BasicAuthenticationBackend(BaseBackend):
    """Basic authentication."""

    def authenticate(self, request, provider, username=None, password=None):
        """Authenticate a :class:`Subject` with a username and password."""
        return provider.check_password(username, password)

    @ioc.inject('subjects', 'iam.SubjectRepository') # pragma: no cover
    def get_user(self, lsid, subjects):
        """Return the :term:`Subject` identified by `lsid`."""
        return subjects.get(pk=lsid)
