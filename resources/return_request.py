import traceback
import datetime
from flask_restful import Resource
from flask import request

from db import db
from schemas.return_request import ReturnRequestSchema
from models.return_request import ReturnRequestModel
from models.transaction import TransactionModel
from models.book import BookModel
from models.user import UserModel

return_request_schema = ReturnRequestSchema()
return_request_list_schema = ReturnRequestSchema(many=True)

class ReturnRequestList(Resource):
    @classmethod
    def get(cls,user_id):
        requests = ReturnRequestModel.find_by_received_id(user_id)
        return {"requests": return_request_list_schema.dump(requests)}, 200

class ReturnRequest(Resource):
    @classmethod
    def post(cls, book_id):
        book = BookModel.find_by_id(book_id)
        if not book:
            return {"message":"Book not found"}, 404
        if not book.is_borrowed:
            return {"message":"Book not borrowed"}, 400
        transaction = TransactionModel.find_issued_book(book_id)
        if not transaction:
            return {"message": "Transaction not found"}, 404
        req = ReturnRequestModel.find_by_book_id(book_id)
        if req:
            return {"message":"Already sent"},400
        req = ReturnRequestModel(date=datetime.datetime.now(), sent_by=transaction.lent_to, received_by=transaction.borrowed_from, book_id=book_id)
        req.save_to_db()
        return {"message": "Return request sent"}, 200

class ReturnRequestResponse(Resource):
    @classmethod
    def post(cls, request_id):
        data = request.get_json()
        req = ReturnRequestModel.find_by_id(request_id)
        if not req:
            return {"message": "no request found"}, 404
        if data['response']:
            req.book.is_borrowed=False
            transaction = TransactionModel.find_issued_book(req.book_id)
            if not transaction:
                return {"message": "transaction not found"}, 404
            transaction.return_date=datetime.datetime.now()
            if transaction.book.till_date < datetime.datetime.now():
                interval = transaction.book.till_date - datetime.datetime.now
                user = UserModel.find_by_id(transaction.lent_to)
                user.merit_point = user.merit_point + (interval.days+1)*2
                user.save_to_db()
            transaction.save_to_db()
            req.delete_from_db()
            return {"message": "Accepted request"}, 200
        else:
            req.delete_from_db()
            return {"message": "Rejected request"}, 200