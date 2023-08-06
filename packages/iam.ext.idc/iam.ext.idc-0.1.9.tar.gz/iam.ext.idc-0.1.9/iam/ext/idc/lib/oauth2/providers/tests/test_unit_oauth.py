# pylint: skip-file
from iam.ext.idc.lib.oauth2.providers.generic import GenericOAuth2Provider
from .base import BaseProviderTestcase


PROVIDER_RESOURCE = """
apiVersion: v1alpha1
kind: OAuth2Provider
metadata:
  name: test-oauth-basic
spec:
  description: Basic OAuth2
  credentials:
    id: foo
    secret: bar
  defaultProvider: true
  providerMetadata:
    authorizeUrl: https://api.twitter.com/oauth/authenticate
    baseUrl: https://api.twitter.com/1.1/
    requestToken:
      url: https://api.twitter.com/oauth/request_token
      #params: null
    accessToken:
      url: https://api.twitter.com/oauth/access_token
      #params: null
    #refreshToken:
    #  url: null
"""


class GenericOAuth2ProviderTestCase(BaseProviderTestcase):
    provider_resource = PROVIDER_RESOURCE
    provider_class = GenericOAuth2Provider
    __test__ = True
