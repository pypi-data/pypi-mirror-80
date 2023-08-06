# pylint: skip-file
"""Declares :class:`BaseProvider`."""
from django.contrib.auth import authenticate
from django.contrib.auth import login


class BaseProvider:
    """The base class for all Single Sign-on (SSO) providers."""

    @classmethod
    def fromresource(cls, resource, *args, **kwargs):
        """Create a new :class:`BaseProvider` from a provider
        resource.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def __init__(self, spec):
        self._spec = spec

    def authenticate(self, request, *args, **kwargs):
        """Authenticate a :term:`Subject` using the Django authentication system."""
        return authenticate(request, *args, **kwargs) # pragma: no cover

    def login(self, request, subject):
        """Login a :term:`Subject` using the Django authentication system."""
        login(request, subject) # pragma: no cover

    def is_default(self):
        """Return a boolean indicating if the provider has marked itself as
        a default provider.
        """
        return bool(self._spec.get('is_default'))

    def is_enabled(self):
        """Return a boolean indicating if the provider is enabled."""
        return True
