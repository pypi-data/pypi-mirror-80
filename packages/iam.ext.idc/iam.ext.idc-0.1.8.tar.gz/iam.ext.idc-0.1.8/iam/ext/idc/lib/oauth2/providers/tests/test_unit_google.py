# pylint: skip-file
from iam.ext.idc.lib.oauth2.providers.google import GoogleOIDCProvider
from .base import BaseProviderTestcase


PROVIDER_RESOURCE = """
apiVersion: testing
kind: OAuth2Provider
metadata:
  name: test-oidc-google
type: accounts.google.com
spec:
  description: Test Provider
  credentials:
    id: foo
    secret: bar
  scope:
  - email
  - profile
"""


class OIDCGenericProviderTestCase(BaseProviderTestcase):
    environ = {
        'GOOGLE_OAUTH_CLIENT_ID': "foo",
        'GOOGLE_OAUTH_CLIENT_SECRET': "bar"
    }
    provider_resource = PROVIDER_RESOURCE
    provider_class = GoogleOIDCProvider
    __test__ = True

    def test_get_asserted_subject_id(self):
        p = self.registry.get(self.resource['metadata']['name'])
        asid = p.get_asserted_subject_id({'sub': '1', 'aud': 'foo'})
        self.assertEqual(asid, "1@foo")

    def test_fromenv(self):
        p = self.provider_class.fromenv(self.environ)
        self.assertEqual(p.description, "Google")
