from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserQuerySchema(Schema):
    id = fields.Int(required=True)


class UserQueryOptionalSchema(Schema):
    id = fields.Int(required=False)

class SuccessMessageSchema(Schema):
    message = fields.Str(dump_only=True)
