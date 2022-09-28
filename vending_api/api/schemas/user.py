from vending_api.extensions import db, ma
from vending_api.models import User
from vending_api.models.user import RoleEnum


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    role = ma.Enum(enum=RoleEnum, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)

