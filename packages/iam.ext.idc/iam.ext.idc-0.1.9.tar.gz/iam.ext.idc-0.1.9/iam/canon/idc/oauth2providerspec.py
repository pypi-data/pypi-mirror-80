"""Declares :class:`OAuth2ProviderSpecSchema`."""
import marshmallow
import marshmallow.fields

from .oauth2credentials import OAuth2CredentialsSchema
from .oauth2providermetadata import OAuth2ProviderMetadataSchema


class OAuth2ProviderSpecSchema(marshmallow.Schema):
    """Declares a schema for ``OAuth2ProviderSpec`` resources."""
    description = marshmallow.fields.String(
        required=True,
        data_key='description'
    )

    scope = marshmallow.fields.List(
        marshmallow.fields.String,
        required=False,
        default=list,
        missing=list
    )

    credentials = marshmallow.fields.Nested(
        OAuth2CredentialsSchema,
        required=True
    )

    superusers = marshmallow.fields.List(
        marshmallow.fields.String,
        required=False,
        missing=list,
        default=list
    )

    external = marshmallow.fields.Boolean(
        required=False,
        missing=False,
        default=False
    )

    is_default = marshmallow.fields.Boolean(
        required=False,
        missing=False,
        default=False,
        data_key='defaultProvider'
    )

    url = marshmallow.fields.URL(
        required=False,
        missing=None,
        default=None,
        data_key='metadataUrl'
    )

    metadata = marshmallow.fields.Nested(
        OAuth2ProviderMetadataSchema,
        required=False,
        missing=None,
        default=None,
        data_key='providerMetadata'
    )
