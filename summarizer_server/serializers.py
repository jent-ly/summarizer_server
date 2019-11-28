from marshmallow import Schema, fields


class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Str()
    gaia = fields.Str()


class FeedbackSchema(Schema):
    id = fields.Integer(dump_only=True)
    url = fields.Str()
    score = fields.Integer()
    description = fields.Str()
    timestamp = fields.DateTime()
    account_id = fields.Integer()
