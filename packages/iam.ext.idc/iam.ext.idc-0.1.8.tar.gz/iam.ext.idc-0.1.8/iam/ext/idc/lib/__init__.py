# pylint: skip-file
from .loaders import EnvironmentLoader
from .loaders import SecretsDirectoryLoader
from .registry import BaseIdentityProviverRegistry


class IdentityProvidersRegistry(BaseIdentityProviverRegistry):
    """Maintains a registry of all defined identity providers."""
    pass
