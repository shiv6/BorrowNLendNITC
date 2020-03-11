from ma import ma
from models.borrow_request import BorrowRequestModel
from db import db

class BorrowRequestSchema(ma.ModelSchema):
    class Meta:
        model = BorrowRequestModel
        sqla_session = db.session
        dump_only = ("id","received_by")
        datetimeformat = "%d-%m-%Y"