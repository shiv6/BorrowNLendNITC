import traceback
from flask_restful import Resource
from flask import request
import datetime

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

class CheckAlert(Resource):
    @classmethod
    def get(cls,user_id):
        transactions = TransactionModel.find_due_book(user_id)
        for transaction in transactions:
            if transaction.book.till_date < datetime.datetime.now():
                return {"due":True}, 200
        return {"due":False}, 200