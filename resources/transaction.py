import traceback
from flask_restful import Resource
import flask import requests

from db import db
from schemas.transaction import TransactionSchema
from models.transaction import TransactionModel

transaction_schema = TransactionSchema()
transaction_list_schema = TransactionSchema(many=True)

class TransactionList(Resource):
    @classmethod
    def get(cls):
        return {"transactions": transaction_list_schema.dump(TransactionModel.find_all())}, 200