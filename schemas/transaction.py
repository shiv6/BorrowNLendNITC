from ma import ma
from models.transaction import TransactionModel
from db import db

class TransactionSchema(ma.ModelSchema):
    class Meta:
        model = TransactionModel
        sqla_session = db.session
        dump_only = ("id",)
        datetimeformat = "%d-%m-%Y"