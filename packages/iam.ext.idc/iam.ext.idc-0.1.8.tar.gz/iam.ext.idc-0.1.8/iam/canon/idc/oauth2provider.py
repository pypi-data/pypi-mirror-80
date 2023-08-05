# pylint: disable=R0801
"""Declares :class:`OAuth2ProviderSchema`."""
import marshmallow
import marshmallow.fields

from .oauth2providerspec import OAuth2ProviderSpecSchema
from .objectmeta import ObjectMetaSchema


class OAuth2ProviderSchema(marshmallow.Schema):
    """Declares a schema for ``OAuth2Provider`` resources."""
    apiVersion = marshmallow.fields.String(
        required=True
    )

    kind = marshmallow.fields.String(
        required=True
    )

    metadata = marshmallow.fields.Nested(
        ObjectMetaSchema,
        required=True
    )

    spec = marshmallow.fields.Nested(
        OAuth2ProviderSpecSchema,
        required=True
    )

    type = marshmallow.fields.String(
        required=False,
        missing="iam.unimatrixone.io/oidc",
        default="iam.unimatrixone.io/oidc"
    )
