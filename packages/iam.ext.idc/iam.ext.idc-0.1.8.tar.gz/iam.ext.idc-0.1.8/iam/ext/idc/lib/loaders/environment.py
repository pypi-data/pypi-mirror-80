# pylint: disable=R0903
"""Declares :class:`EnvironmentLoader`."""
import os

from .base import BaseLoader

from ..static import StaticPasswordProvider
from ..oauth2.providers import GoogleOIDCProvider


class EnvironmentLoader(BaseLoader):
    """Loads providers from environment variables."""
    provider_classes = [
        StaticPasswordProvider,
        GoogleOIDCProvider
    ]

    def load(self, env=None): # pylint: disable=W0221
        """Invoke the ``fromenv()`` method on :attr:`provider_classes`
        to construct a list of providers.
        """
        providers = []
        for cls in self.provider_classes:
            try:
                providers.append(cls.fromenv(env or os.environ))
            except KeyError:
                continue
        return providers
