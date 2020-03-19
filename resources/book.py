import traceback
from flask_restful import Resource
from flask import request

from db import db
from schemas.book import BookSchema
from models.book import BookModel
from models.transaction import TransactionModel

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

class AddBook(Resource):
    @classmethod
    def post(cls):
        book = book_schema.load(request.get_json())
        try:
            book.save_to_db()
            return {
                "message": "Book Added",
                "book_id":book.id
                }, 201
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
        if book.is_borrowed:
            return {"message": "Borrowed book can\'t be deleted"}, 400
        book.delete_from_db()
        return {"message":"Book deleted"}, 200

class BookList(Resource):
    @classmethod
    def get(cls):
        return {"books": book_list_schema.dump(BookModel.find_all())}, 200

class DueBooks(Resource):
    @classmethod
    def get(cls, user_id):
        transactions = TransactionModel.find_due_book(user_id)
        books=[]
        for transaction in transactions:
            books.append(transaction.book)
        return {"books":book_list_schema.dump(books)},200

class UserBookList(Resource):
    @classmethod
    def get(cls,user_id):
        return {"books": book_list_schema.dump(BookModel.find_by_user_id(user_id))}, 200

class BookSearch(Resource):
    @classmethod
    def get(cls,user_id,category,keyword):
        books= BookModel.search_by_category(user_id,category,keyword)
        return {"books":book_list_schema.dump(books)},200