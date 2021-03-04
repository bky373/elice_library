from elice_library.database.config import ma
from marshmallow import fields, INCLUDE


class CommentSchema(ma.Schema):
    class Meta:
        unknown = INCLUDE

    content = fields.Str(required=True)
    rating = fields.Int(required=True)
