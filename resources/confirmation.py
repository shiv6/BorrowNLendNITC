from time import time
import traceback

from flask_restful import Resource
from flask import render_template, make_response

from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema
from libs.mailgun import MailGunException

confirmation_schema = ConfirmationSchema()

class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return { "message": 'confirmation_not_found' }, 404
        
        if confirmation.expired:
            return { "message": 'confirmation_link_expired' }, 400

        if confirmation.confirmed:
            return { "message": 'confirmation_already_confirmed' }, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = { "Content-Type": "text/html" }

        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers
        )


class ConfirmationByUser(Resource):
    @classmethod
    def get(self, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return { 'message': gettext('user_not_found') }, 404
        
        return {
            "current_time": int(time()),
            "confirmation": [
                confirmation_schema.dump(each)
                for each in user.confirmation.order_by(ConfirmationModel.expire_at)
            ]
        }, 200

    @classmethod
    def post(self,user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return { "message": 'user_not_found' }, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return { 'message': 'confirmation_already_confirmed' }, 400
                confirmation.force_to_expire()
            
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return { 'message': 'confirmation_resend_successful' }, 201
        except MailGunException as e:
            return { 'message':str(e) }, 500
        except:
            traceback.print_exc()
            return { 'message': 'confirmation_resend_fail' }, 500