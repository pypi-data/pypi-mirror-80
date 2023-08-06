"""Declares :class:`OAuth2ProviderMetadataSchema`."""
import marshmallow
import marshmallow.fields


class OAuth2ProviderMetadataSchema(marshmallow.Schema):
    """Decalres a schema for ``OAuth2ProviderMetadataS`` resources."""
    authorize_url = marshmallow.fields.URL(
        required=True,
        data_key='authorizeUrl'
    )

    base_url = marshmallow.fields.URL(
        required=True,
        data_key='baseUrl'
    )

    request_token = marshmallow.fields.Nested(
        'OAuth2TokenURLConfigSchema',
        required=True,
        data_key='requestToken'
    )

    access_token = marshmallow.fields.Nested(
        'OAuth2TokenURLConfigSchema',
        required=True,
        data_key='accessToken'
    )


class OAuth2TokenURLConfigSchema(marshmallow.Schema):
    """Declares a schema to validate metadata URLs."""
    url = marshmallow.fields.URL(required=True)
    params = marshmallow.fields.Dict(
        allow_none=True,
        required=False,
        missing=None,
        default=None
    )
