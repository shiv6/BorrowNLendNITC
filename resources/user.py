import traceback
import datetime
from flask_restful import Resource, reqparse, jwt_refresh_token_required
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_raw_jwt

from schemas.user import UserSchema
from models.user import UserModel
from models.confirmation import ConfirmationModel

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())
        
        if UserModel.find_by_email(user.email):
            return {"message": "Email already exist"}, 400
        
        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            res = user.send_confirmation_email()
            return {"message": "User created"}, 201
        except:
            traceback.print_exc()
            # user.delete_from_db()
            return { "message": "User creating error"}, 500

class UserLogin(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        user = UserModel.find_by_email(email=args['email'])

        if user and safe_str_cmp(args['password'],user.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                expires = datetime.timedelta(minutes=60)
                access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token":refresh_token, "user_id":user.id}, 200
            return {"message": "User not confirmed"}, 400
        return {"message": "user invalid crendential"}, 401

class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": 'user_logged_out'}, 200


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user_schema.dump(user),200
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200

class UserList(Resource):
    @classmethod
    def get(cls):
        return {"users": user_list_schema.dump(UserModel.find_all())},200

class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
