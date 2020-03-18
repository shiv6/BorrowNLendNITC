from ma import ma
from marshmallow_sqlalchemy import fields
from models.book import BookModel
from schemas.user import UserSchema
from db import db

class BookSchema(ma.ModelSchema):
    class Meta:
        model = BookModel
        sqla_session = db.session
        dump_only = ("id","is_borrowed")
        datetimeformat = "%d-%m-%Y"
    owner = fields.Nested(UserSchema)