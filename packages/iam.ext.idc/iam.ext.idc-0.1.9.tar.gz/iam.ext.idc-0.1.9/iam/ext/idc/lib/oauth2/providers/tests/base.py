# pylint: skip-file
import os
import tempfile
import unittest

import ioc
import unimatrix.lib.test
import yaml
from authlib.integrations.django_client import OAuth

from iam.ext.idc.lib import SecretsDirectoryLoader
from iam.ext.idc.lib import IdentityProvidersRegistry


@unimatrix.lib.test.unit
class BaseProviderTestcase(unittest.TestCase):
    __test__ = False

    @classmethod
    def setUpClass(cls):
        cls.secdir = tempfile.mkdtemp()
        os.makedirs(os.path.join(cls.secdir, 'iam.unimatrixone.io/providers'))
        cls.fp = os.path.join(cls.secdir,
            "iam.unimatrixone.io/providers", 'providers.yaml')
        with open(cls.fp, 'w') as f:
            f.write(cls.provider_resource)
        ioc.provide('OAuth2Registry', OAuth(), force=True)

    def setUp(self):
        self.registry = IdentityProvidersRegistry([
            SecretsDirectoryLoader(secdir=self.secdir)
        ])
        self.resource = yaml.safe_load(self.provider_resource)

    def test_parse_from_resource(self):
        p = self.registry.get(self.resource['metadata']['name'])
        self.assertIsInstance(p, self.provider_class)

    def test_name_equals_resource_name(self):
        p = self.registry.get(self.resource['metadata']['name'])
        self.assertEqual(p.name, self.resource['metadata']['name'])

    def test_description_equals_resource_description(self):
        p = self.registry.get(self.resource['metadata']['name'])
        self.assertEqual(p.description, self.resource['spec']['description'])
