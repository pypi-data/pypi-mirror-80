# pylint: disable=invalid-name,no-self-use
"""Declares :class:`SubjectRepository`."""
from django.apps import apps


class SubjectRepository:
    """Provides an interface to lookup :class:`~iam.ext.idc.models.AssertedSubject`
    objects.
    """
    model_class = 'idc.AssertedSubject'

    @property
    def DoesNotExist(self):
        """Proxy to Django :exc:`DoesNotExist`."""
        return self.model.DoesNotExist

    @property
    def model(self):
        """Return the Django model class used by this repository."""
        return apps.get_model(self.model_class)

    def exists(self, pk):
        """Return a boolean indicating if the entity identified by
        primary key `pk` exists.
        """
        return self.model.objects.filter(pk=pk).exists()

    def get(self, *args, **kwargs):
        """Return a single entity using the provided lookup parameters."""
        return self.model.objects.get(*args, **kwargs)

    def persist(self, dao):
        """Persists a Data Access Object (DAO) to the storage backend."""
        dao.save()
