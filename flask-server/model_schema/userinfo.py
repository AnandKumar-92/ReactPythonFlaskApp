from marshmallow import Schema, fields

class UserInfoSchema(Schema):
    id = fields.Str()
    firstname = fields.Str()
    lastname = fields.Str()
    Avatar_url = fields.Str()


userinfo_schema = UserInfoSchema()
usersinfo_schema = UserInfoSchema(many=True)