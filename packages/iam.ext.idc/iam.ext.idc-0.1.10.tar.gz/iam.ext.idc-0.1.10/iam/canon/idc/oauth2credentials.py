"""Declares :class:`OAuth2CredentialsSchema`."""
import marshmallow
import marshmallow.fields


class OAuth2CredentialsSchema(marshmallow.Schema):
    """Declares a schema for ``OAuth2Credentials`` resources."""
    id = marshmallow.fields.String(required=True)
    secret = marshmallow.fields.String(required=True)
