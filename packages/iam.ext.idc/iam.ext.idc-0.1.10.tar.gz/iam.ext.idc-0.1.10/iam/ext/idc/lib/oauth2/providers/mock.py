# pylint: skip-file
"""Declares :class:`MockOAuth2Provider`."""
import ioc
from django.http import HttpResponseRedirect

from .generic import GenericOAuth2Provider


class MockOAuth2Provider(GenericOAuth2Provider):

    @property
    def name(self):
        return self._metadata['name']

    @property
    def description(self):
        return self._spec['description']

    @classmethod
    def fromresource(cls, resource, *args, **kwargs):
        return cls(resource['metadata'], cls.schema.load(resource['spec']))

    def __init__(self, metadata, spec):
        self._metadata = metadata
        self._spec = spec

    @ioc.inject('subjects', 'iam.SubjectRepository')
    def get_asserted_subject(self, request, subjects):
        annotations = self._metadata.get('annotations') or {}
        return subjects.get(pk=annotations['lsid'])\
            if annotations.get('lsid')\
            else None

    def start_authentication(self, request, redirect_to):
        return HttpResponseRedirect(redirect_to)
