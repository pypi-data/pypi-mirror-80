"""Declares :class:`IdentityConsumerConfig`."""
import ioc
import ioc.loader
from authlib.integrations.django_client import OAuth
from django.apps import AppConfig
from django.apps import apps
from django.conf import settings

from .infra import SubjectRepository


class IdentityConsumerConfig(AppConfig):
    """Configures the :mod:`iam.ext.idc` package."""
    name = 'iam.ext.idc'
    label = 'idc'
    verbose_name = "IAM - Identity Consumer"
    default_loaders = [
        'iam.ext.idc.lib.EnvironmentLoader',
        'iam.ext.idc.lib.SecretsDirectoryLoader'
    ]

    def ready(self):
        """Invoked when the Django app registry has loaded all
        apps.
        """
        ioc.provide('OAuth2Registry', OAuth())
        ioc.provide('iam.SubjectRepository', SubjectRepository())
        ioc.provide('iam.SubjectFactory', apps.get_model('idc.AssertedSubject'))

        loaders = []
        ioc.provide('iam.IdentityProviderLoaders', loaders)
        for qualname in getattr(settings, 'IAM_IDP_LOADERS', self.default_loaders):
            cls = ioc.loader.import_symbol(qualname)
            loaders.append(cls())
