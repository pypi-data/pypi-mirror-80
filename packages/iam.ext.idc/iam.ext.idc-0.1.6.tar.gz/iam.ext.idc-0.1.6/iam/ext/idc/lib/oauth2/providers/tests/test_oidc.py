# pylint: skip-file
from iam.ext.idc.lib.oauth2.providers.generic import GenericOAuth2Provider
from .base import BaseProviderTestcase


PROVIDER_RESOURCE = """
apiVersion: testing
kind: OAuth2Provider
metadata:
  name: test-oidc-generic
spec:
  description: Test Provider
  credentials:
    id: foo
    secret: bar
  scope:
  - email
  - profile
  metadataUrl: https://example.com/metadata
"""


class OIDCGenericProviderTestCase(BaseProviderTestcase):
    provider_resource = PROVIDER_RESOURCE
    provider_class = GenericOAuth2Provider
    __test__ = True
