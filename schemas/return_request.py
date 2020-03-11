from ma import ma
from models.return_request import ReturnRequestModel
from db import db

class ReturnRequestSchema(ma.ModelSchema):
    class Meta:
        model = ReturnRequestModel
        sqla_session = db.session
        dump_only = ("id",)
        datetimeformat = "%d-%m-%Y"