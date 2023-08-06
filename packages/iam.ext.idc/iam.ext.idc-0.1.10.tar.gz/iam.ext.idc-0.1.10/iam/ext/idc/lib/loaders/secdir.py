# pylint: disable=C0103
"""Declares :class:`SecretsDirectoryLoader`."""
import os

import yaml

from iam.canon.idc import ResourceSchema
from ..oauth2 import get_oauth2_provider
from .base import BaseLoader


class SecretsDirectoryLoader(BaseLoader):
    """Loads identity provider configurations from the application secrets
    directory.
    """
    schema_class = ResourceSchema
    provider_factories = {
        'OAuth2Provider': get_oauth2_provider,
    }

    @property
    def secdir(self):
        """Returns the directory name holding the secrets (i.e. provider
        configurations) used by the :class:`BaseIdentityProviverRegistry`.
        """
        return os.path.join(self.__secdir, "iam.unimatrixone.io/providers")

    def __init__(self, secdir=None):
        self.__secdir = secdir or os.environ['APP_SECDIR']
        self.__schema = self.schema_class()

    def get_provider(self, resource):
        """Instantiate a new :class:`Provider` from the parameters
        specified in `resource`.
        """
        f = self.get_provider_factory(resource) # pylint: disable=C0103
        return f(resource)

    def get_provider_factory(self, resource):
        """Returns the provider implementation class for the given
        resource.
        """
        return self.provider_factories[ resource['kind'] ]

    def is_supported_resource(self, resource):
        """Return a boolean indicating if the resource is supported by this
        provider.
        """
        return resource.get('kind') in list(self.provider_factories.keys())

    def load(self):
        """Iterate over all YAML files in the secrets directory and instantiate
        providers.
        """
        providers = []
        if not os.path.exists(self.secdir): # pragma: no cover
            return providers

        for fn in os.listdir(self.secdir):
            fp = os.path.join(self.secdir, fn)
            for doc in yaml.load_all(open(fp), Loader=yaml.SafeLoader): # pylint: disable=C0103
                if not self.is_supported_resource(doc): # pragma: no cover
                    # Silently ignore unrecognized documents.
                    continue
                providers.append(self.get_provider(doc))

        return providers
