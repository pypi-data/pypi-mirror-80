"""The :mod:`iam.ext.idc.lib.oauth2` implements OAuth2."""
from collections import defaultdict

import ioc

from .providers import GenericOAuth2Provider
from .providers import OIDCGenericProvider
from .providers import GoogleOIDCProvider
from .providers import MockOAuth2Provider


PROVIDER_CLASSES = defaultdict(lambda: GenericOAuth2Provider, {
    'accounts.google.com': GoogleOIDCProvider,
    'mock': MockOAuth2Provider
})


@ioc.inject('oauth2', 'OAuth2Registry')
def get_oauth2_provider(resource, oauth2):
    """Return an OAuth2 provider implementation class based on the type
    member of `resource.
    """
    return PROVIDER_CLASSES[ resource.get('type') ].fromresource(resource, oauth2)
