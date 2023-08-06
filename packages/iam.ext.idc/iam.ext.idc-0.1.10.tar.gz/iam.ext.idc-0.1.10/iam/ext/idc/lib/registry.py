# pylint: disable=no-self-use,unused-argument,invalid-name
"""Declares :class:`BaseIdentityProviverRegistry`."""
import abc
import itertools
from collections import OrderedDict


NOT_LOADED = object()


class BaseIdentityProviverRegistry(metaclass=abc.ABCMeta):
    """The base class for all identity provider registries."""

    def __init__(self, loaders, *args, **kwargs):
        self.__providers = NOT_LOADED
        self.__default = None
        self.__loaders = loaders

    def enabled(self):
        """Return a list containing all enabled providers."""
        if self.__providers == NOT_LOADED: # pragma: no cover
            self.load_providers()
        return list([x for x in self.__providers.values() if x.is_enabled()])

    def lookup(self, name):
        """Return the identity provider identified by `name`."""
        return self.__providers[name]

    def load_providers(self):
        """Load the providers of the specified :attr:`resource_kind` from
        the secrets directory.
        """
        providers = OrderedDict()
        for provider in itertools.chain(*map(lambda x: x.load(), self.__loaders)):
            if provider.is_default():
                self.__default = provider
            providers[provider.name] = provider

        self.__providers = providers

        # If there is no default provider at this point, select the first loaded
        # from the persistent configuration.
        if self.__default is None and bool(providers):
            self.__default = list(providers.values())[0]

    def get(self, name):
        """Return the identity provider identified by `name`. Load the providers
        from the persistent storage backend if not present.
        """
        if self.__providers == NOT_LOADED:
            self.load_providers()
        return self.lookup(name)

    def get_default_provider(self):
        """Return the default provider configured for this registry."""
        if self.__providers == NOT_LOADED: # pragma: no cover
            self.load_providers()
        return self.__default
