from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_cors import CORS
import traceback
import smtplib

from db import db
from ma import ma
from blacklist import BLACKLIST

app = Flask(__name__)

CORS(app)

# load_dotenv(".env",verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

@app.errorhandler(500)
def internal_error(e):
    traceback.print_exc()
    return {"message": "internal server error"}, 500

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

from resources.user import User, UserList, UserRegister, UserLogin, UserLogout, TokenRefresh, UserBlock, UserBlockRequest
from resources.book import Book,AddBook, BookList, BookSearch, UserBookList, DueBooks
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.borrow_request import BorrowRequest, BorrowRequestList, BorrowRequestResponse
from resources.return_request import ReturnRequest, ReturnRequestList, ReturnRequestResponse
from resources.transaction import TransactionSummary,CheckAlert

# ADD RESOURCES HERE

class SendMail(Resource):
    @classmethod
    def get(cls):
        sender = 'hello@nakshatra20.com'
        receivers = ['careeratedjing@gmail.com']

        message = """From: From Person <from@fromdomain.com>
        To: To Person <to@todomain.com>
        Subject: SMTP e-mail test

        This is a test e-mail message.
        """
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)         
            return {"message":"sent success"},200
        except:
            return {"message":"sent failed"},400

api.add_resource(SendMail,"/sendmail")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')
api.add_resource(UserBlock,'/blocking/<string:block_status>/<int:user_id>')
api.add_resource(UserBlockRequest,'/block/book/<int:book_id>')
api.add_resource(Book,'/book/<int:book_id>')
api.add_resource(BookList,'/books')
api.add_resource(AddBook,'/book')
api.add_resource(TransactionSummary,'/user/<int:user_id>/summary')
api.add_resource(DueBooks,'/user/<int:user_id>/duebooks')
api.add_resource(CheckAlert,'/user/<int:user_id>/isdue')
api.add_resource(UserBookList,'/user/<int:user_id>/books')
api.add_resource(BookSearch,'/user/<int:user_id>/search/<string:category>/<string:keyword>')
api.add_resource(Confirmation, "/user_confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(BorrowRequestList,'/user/<int:user_id>/borrowrequests')
api.add_resource(BorrowRequest,'/borrowrequest')
api.add_resource(BorrowRequestResponse, '/borrowrequest/<int:request_id>/response')
api.add_resource(ReturnRequestList,'/user/<int:user_id>/returnrequests')
api.add_resource(ReturnRequest, '/book/<int:book_id>/returnrequest')
api.add_resource(ReturnRequestResponse,'/returnrequest/<int:request_id>/response')

db.init_app(app)
ma.init_app(app)

if __name__=="__main__":
    app.run(port=5000)