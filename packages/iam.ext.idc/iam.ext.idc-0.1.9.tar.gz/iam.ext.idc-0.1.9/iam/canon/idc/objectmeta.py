"""Declares :class:`ObjectMetaSchema`."""
import marshmallow
import marshmallow.fields


class ObjectMetaSchema(marshmallow.Schema):
    """Declares a schema for `ObjectMetadata` resources."""
    namespace = marshmallow.fields.String(
        required=False,
        default="",
        missing=""
    )

    name = marshmallow.fields.String(
        required=True
    )

    annotations = marshmallow.fields.Dict(
        required=False,
        missing=dict
    )
