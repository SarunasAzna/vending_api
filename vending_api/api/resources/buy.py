from flask import abort, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from vending_api.api.schemas import UserSchema, BuySchema
from vending_api.extensions import db
from vending_api.models import User, Product
from flask_jwt_extended import get_jwt_identity


class BuyResource(Resource):

    method_decorators = [jwt_required()]

    def post(self):
        payload = request.json
        schema = BuySchema()
        msg = schema.validate(payload)
        user_id = get_jwt_identity()
        buyer = User.query.get_or_404(user_id)

        if msg:
            abort(400, msg)
        product = Product.query.get_or_404(payload["productId"])
        amount = payload["amount"]
        try:
            change = product.buy(amount, buyer)
        except ValueError as e:
            abort(400, str(e))
        except PermissionError as e:
            abort(403, str(e))
        db.session.commit()
        return {
            "Message": "Bought",
            "product": product.productName,
            "change": change,
        }
