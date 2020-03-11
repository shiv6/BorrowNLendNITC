import traceback
from flask_restful import Resource
from flask import request

from db import db
from schemas.book import BookSchema
from models.book import BookModel

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

class AddBook(Resource):
    @classmethod
    def post(cls):
        book = book_schema.load(request.get_json())
        try:
            book.save_to_db()
            return {"message": "Book Added"}, 201
        except:
            traceback.print_exc()
            book.delete_from_db()
            return {"message": "Book not created"}, 500

class Book(Resource):
    @classmethod
    def get(cls,book_id):
        book = BookModel.find_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404    
        return book_schema.dump(book), 200
    
    @classmethod
    def delete(cls, book_id):
        book = BookModel.find_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404    
        book.delete_from_db()
        return {"message":"Book deleted"}, 200

class BookList(Resource):
    @classmethod
    def get(cls):
        return {"books": book_list_schema.dump(BookModel.find_all())}, 200