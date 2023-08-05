# pylint: skip-file
"""Declares :class:`BaseLoader`."""
import abc


class BaseLoader:
    """The base class for all identity provider configuration loaders."""

    @abc.abstractmethod
    def load(self):
        """Loads identity provider configurations from specific sources."""
        raise NotImplementedError
