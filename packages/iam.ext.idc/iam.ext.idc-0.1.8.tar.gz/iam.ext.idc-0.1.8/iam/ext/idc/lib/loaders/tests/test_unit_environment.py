# pylint: skip-file
import unittest

import ioc
import unimatrix.lib.test
from authlib.integrations.django_client import OAuth

from ..environment import EnvironmentLoader


@unimatrix.lib.test.unit
class EnvironmentLoaderTestCase(unittest.TestCase):

    def setUp(self):
        ioc.provide('OAuth2Registry', OAuth(), force=True)

    def test_load_from_environment(self):
        loader = EnvironmentLoader()
        providers = loader.load({
            'GOOGLE_OAUTH_CLIENT_ID': "foo",
            'GOOGLE_OAUTH_CLIENT_SECRET': "bar"
        })
        self.assertTrue(len(providers) == 1)

    def test_load_from_environment_with_empty(self):
        loader = EnvironmentLoader()
        providers = loader.load({})
        self.assertEqual(len(providers), 0)
