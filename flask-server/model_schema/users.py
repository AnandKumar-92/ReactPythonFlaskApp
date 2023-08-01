from marshmallow import Schema, fields

# Schema
class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    email = fields.Str()
    role=fields.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)