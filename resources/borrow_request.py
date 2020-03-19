import traceback
import datetime
from flask_restful import Resource
from flask import request

from db import db
from schemas.borrow_request import BorrowRequestSchema
from models.borrow_request import BorrowRequestModel
from models.transaction import TransactionModel
from models.book import BookModel

borrow_request_schema = BorrowRequestSchema()
borrow_request_list_schema = BorrowRequestSchema(many=True)

class BorrowRequestList(Resource):
    @classmethod
    def get(cls,user_id):
        requests = BorrowRequestModel.find_by_recieved_id(user_id)
        return {"requests": borrow_request_list_schema.dump(requests)}, 200

class BorrowRequest(Resource):
    @classmethod
    def post(cls):
        req = borrow_request_schema.load(request.get_json())
        req.date = datetime.datetime.now()
        book = BookModel.find_by_id(req.book_id)
        if BorrowRequestModel.check_if_exist(req.book_id,req.sent_by):
            return {"message": "already sent"}, 400
        req.received_by = book.user_id
        req.save_to_db()
        return {"message": "borrow request sent"}, 200

class BorrowRequestResponse(Resource):
    @classmethod
    def post(cls,request_id):
        data = request.get_json()
        req = BorrowRequestModel.find_by_id(request_id)
        if not req:
            return {"message":"no request found"}, 404
        if data['response']:
            if req.book.is_borrowed:
                return {"message": "already borrowed"}, 400
            req.book.is_borrowed = True
            req.save_to_db()
            transaction = TransactionModel(borrow_date=datetime.datetime.now(), borrowed_from=req.received_by,lent_to = req.sent_by,book_id=req.book_id)
            transaction.save_to_db()
            req.delete_from_db()
            return {"message": "Request Accepted"}, 200
        else:
            req.delete_from_db()
            return {"message": "Request rejected"}, 200