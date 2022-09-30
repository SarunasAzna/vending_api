from flask import abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from vending_api.api.schemas import DepositSchema, UserSchema
from vending_api.extensions import db
from vending_api.models import User


class DepositResource(Resource):

    method_decorators = [jwt_required()]

    def post(self):
        schema = DepositSchema()
        msg = schema.validate(request.json)
        if msg:
            abort(400, msg)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        try:
            user.deposit_coin(request.json["coin"])
        except ValueError as e:
            abort(400, str(e))
        except PermissionError as e:
            abort(403, str(e))
        db.session.commit()
        user_schema = UserSchema()
        return {"message": "Deposited", "user": user_schema.dump(user)}
