from ma import ma
from models.return_request import ReturnRequestModel
from db import db
from marshmallow import fields
from schemas.book import BookSchema
from schemas.user import UserSchema
from models.user import UserModel

user_schema = UserSchema()

class ReturnRequestSchema(ma.ModelSchema):
    class Meta:
        model = ReturnRequestModel
        sqla_session = db.session
        dump_only = ("id",)
        datetimeformat = "%d-%m-%Y"
        include_fk=True
    book = fields.Nested(BookSchema(only=("title","author")))
    sender = fields.Method("add_sender_info")

    def add_sender_info(self, obj):
        return user_schema.dump(UserModel.find_by_id(obj.sent_by))
