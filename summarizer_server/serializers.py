from marshmallow import Schema, fields


class FeedbackSchema(Schema):
    id = fields.Integer(dump_only=True)
    url = fields.Str()
    score = fields.Integer()
    description = fields.Str()
    timestamp = fields.DateTime()
    email = fields.Str()
    gaia = fields.Str()
