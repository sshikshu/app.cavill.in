"""
user schema
"""

from marshmallow import Schema, ValidationError, fields


class UserSchema(Schema):
    created_on = fields.Int()
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    nickname = fields.Str(required=True)
    password = fields.Str(required=True)
    verified = fields.Int()

    def handle_error(self, error: ValidationError, data):
        raise error

user_schema_auth = UserSchema(only=('nickname', 'password'))
user_schema_client = UserSchema(only=('email', 'name', 'nickname', 'password'))
user_schema_external = UserSchema(exclude=('email', 'password'))
user_schema_internal = UserSchema(exclude=('password',))
