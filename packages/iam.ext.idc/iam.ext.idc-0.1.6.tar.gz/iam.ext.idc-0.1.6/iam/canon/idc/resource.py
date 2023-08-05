# pylint: disable=R0801
"""Declares :class:`ResourceSchema`."""
import marshmallow
import marshmallow.fields

from .objectmeta import ObjectMetaSchema


class ResourceSchema(marshmallow.Schema):
    """Declares a schema for identity provider resources."""
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

    spec = marshmallow.fields.Dict(
        required=True
    )

    type = marshmallow.fields.String(
        required=False
    )
