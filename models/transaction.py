from db import db
from sqlalchemy import or_

class TransactionModel(db.Model):
    __tablename__="transactions"

    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.DateTime(), nullable=False)
    return_date = db.Column(db.DateTime())

    borrowed_from = db.Column(db.Integer, nullable=False)
    lent_to = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    book = db.relationship("BookModel", back_populates="transactions")
    
    @classmethod
    def find_issued_book(cls,book_id):
        return cls.query.filter_by(book_id=book_id,return_date=None).first()

    @classmethod
    def find_due_book(cls,user_id):
        return cls.query.filter_by(lent_to=user_id,return_date=None).all()

    @classmethod
    def find_user_summary(cls,user_id):
        return cls.query.filter(or_(TransactionModel.borrowed_from==user_id, TransactionModel.lent_to==user_id)).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()