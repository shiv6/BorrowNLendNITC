from db import db
from models.borrow_request import BorrowRequestModel
from models.return_request import ReturnRequestModel
import datetime

class BookModel(db.Model):
    __tablename__="books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    publication = db.Column(db.String(100), nullable=False)
    edition = db.Column(db.String(100), nullable=False)
    till_date = db.Column(db.DateTime(), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("UserModel", back_populates="books")
    transactions = db.relationship("TransactionModel",cascade = "all,delete", back_populates="book")
    borrow_requests = db.relationship("BorrowRequestModel",cascade = "all,delete", back_populates="book")
    return_requests = db.relationship("ReturnRequestModel",cascade = "all,delete",uselist=False, back_populates="book")


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def search_by_category(cls,user_id,category,keyword):
        key=f'%{keyword}%'
        books=[]
        if category=="author":
            books = BookModel.query.filter(BookModel.author.ilike(key)).filter(BookModel.user_id!=user_id, BookModel.till_date>datetime.datetime.now()).filter_by(is_borrowed=False).all()
        if category=="title":
            books = BookModel.query.filter(BookModel.title.ilike(key)).filter(BookModel.user_id!=user_id, BookModel.till_date>datetime.datetime.now()).filter_by(is_borrowed=False).all()
        if category=="category":
            books = BookModel.query.filter(BookModel.category.ilike(key)).filter(BookModel.user_id!=user_id, BookModel.till_date>datetime.datetime.now()).filter_by(is_borrowed=False).all()
        retbooks=[]
        for book in books:
            if book.owner.is_blocked==False:
                retbooks.append(book)
        return retbooks
