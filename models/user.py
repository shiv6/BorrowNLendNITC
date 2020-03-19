from flask import url_for, request
from db import db
from models.book import BookModel
from models.confirmation import ConfirmationModel
from models.transaction import TransactionModel
from libs.mailgun import Mailgun

class UserModel(db.Model):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(80), nullable=False, unique=True)
    address = db.Column(db.String(120), nullable=False)
    merit_point = db.Column(db.Integer, default=100)
    is_admin = db.Column(db.Boolean, default=False)

    books = db.relationship("BookModel", back_populates="owner")
    confirmation = db.relationship("ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan")
    
    @property
    def most_recent_confirmation(self):
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()


    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_contact(cls, contact):
        return cls.query.filter_by(contact=contact).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('confirmation', confirmation_id=self.most_recent_confirmation.id)
        subject = 'Registration Confirmation',
        text = f'please click the link to confirm your registration: {link}'
        html = f'<html>please click the link to confirm your registration: <a href="{link}">{link}</html>"'
        return Mailgun.send_email([self.email], subject, text, html)
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()