from ma import ma
from marshmallow import fields
from models.transaction import TransactionModel
from db import db
from schemas.user import UserSchema
from models.user import UserModel
from schemas.book import BookSchema

user_schema = UserSchema()

class TransactionSchema(ma.ModelSchema):
    class Meta:
        model = TransactionModel
        sqla_session = db.session
        dump_only = ("id",)
        datetimeformat = "%d-%m-%Y"
        include_fk=True
    book = fields.Nested(BookSchema(only=("title","author","user_id")))
    borrower = fields.Method("add_borrower_info")
    lender = fields.Method("add_lender_info")

    def add_borrower_info(self, obj):
        return user_schema.dump(UserModel.find_by_id(obj.lent_to))

    def add_lender_info(self, obj):
        return user_schema.dump(UserModel.find_by_id(obj.borrowed_from))
