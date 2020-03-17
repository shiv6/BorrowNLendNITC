import traceback
from flask_restful import Resource
from flask import request

from db import db
from schemas.transaction import TransactionSchema
from models.transaction import TransactionModel

transaction_schema = TransactionSchema()
transaction_list_schema = TransactionSchema(many=True)

class TransactionList(Resource):
    @classmethod
    def get(cls):
        return {"transactions": transaction_list_schema.dump(TransactionModel.find_all())}, 200

class TransactionSummary(Resource):
    @classmethod
    def get(cls,user_id):
        return {"transactions": transaction_list_schema.dump(TransactionModel.find_user_summary(user_id))}, 200