from db import db

class ReturnRequestModel(db.Model):
    __tablename__="return_requests"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    sent_by = db.Column(db.Integer, nullable=False)
    received_by = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    book = db.relationship("BookModel", back_populates="return_requests")
    
    @classmethod
    def find_by_received_id(cls,user_id):
        return cls.query.filter_by(received_by=user_id).all()
    
    @classmethod
    def find_by_book_id(cls,book_id):
        return cls.query.filter_by(book_id=book_id).first()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
