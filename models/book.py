from db import db
from models.borrow_request import BorrowRequestModel
from models.return_request import ReturnRequestModel

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
    transactions = db.relationship("TransactionModel", back_populates="book")
    borrow_requests = db.relationship("BorrowRequestModel", back_populates="book")
    return_requests = db.relationship("ReturnRequestModel",uselist=False, back_populates="book")


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()