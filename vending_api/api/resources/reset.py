from flask import abort
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from vending_api.api.schemas import UserSchema
from vending_api.extensions import db
from vending_api.models import User
from flask_jwt_extended import get_jwt_identity


class ResetResource(Resource):

    method_decorators = [jwt_required()]

    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        try:
            user.reset()
        except PermissionError as e:
            abort(403, str(e))
        db.session.commit()
        user_schema = UserSchema()
        return {"message": "Reset", "user": user_schema.dump(user)}
