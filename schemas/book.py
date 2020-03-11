from ma import ma
from models.book import BookModel
from db import db

class BookSchema(ma.ModelSchema):
    class Meta:
        model = BookModel
        sqla_session = db.session
        dump_only = ("id","is_borrowed")
        datetimeformat = "%d-%m-%Y"