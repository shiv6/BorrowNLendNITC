from db import db

class BorrowRequestModel(db.Model):
    __tablename__="borrow_requests"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    sent_by = db.Column(db.Integer, nullable=False)
    received_by = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    book = db.relationship("BookModel", back_populates="borrow_requests")
    
    @classmethod
    def find_by_recieved_id(cls,user_id):
        return cls.query.filter_by(received_by=user_id).all()
    
    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
