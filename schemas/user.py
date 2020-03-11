from ma import ma
from db import db
from models.user import UserModel
from marshmallow import pre_dump

class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        sqla_session = db.session
        load_only = ("password",)
        dump_only = ("id","merit_point","is_admin","confirmation")

    @pre_dump
    def _pre_dump(self, user, **kwargs):
        user.confirmation = [ user.most_recent_confirmation ]
        return user
