from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from vending_api.api.resources import (
    UserList,
    UserResource,
    ProductResource,
    ProductList,
    DepositResource,
    ResetResource,
    BuyResource,
)
from vending_api.api.schemas import UserSchema, ProductSchema, DepositSchema
from vending_api.extensions import apispec

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/user/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/user", endpoint="user")
api.add_resource(ProductResource, "/product/<int:product_id>", endpoint="product_by_id")
api.add_resource(ProductList, "/product", endpoint="product")
api.add_resource(DepositResource, "/deposit", endpoint="deposit")
api.add_resource(ResetResource, "/reset", endpoint="reset")
api.add_resource(BuyResource, "/buy", endpoint="buy")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.components.schema("ProductSchema", schema=ProductSchema)
    apispec.spec.path(view=ProductResource, app=current_app)
    apispec.spec.path(view=ProductList, app=current_app)
    apispec.spec.components.schema("DepositSchema", schema=DepositSchema)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
