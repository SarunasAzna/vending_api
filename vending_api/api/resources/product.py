from flask import request, abort
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from vending_api.api.schemas import ProductSchema
from vending_api.extensions import db
from vending_api.models import Product, User
from vending_api.models.user import RoleEnum
from flask_jwt_extended import get_jwt_identity


def _validate_user_is_owner(product):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.id != product.user_id:
        abort(403,
              description=f"User '{user.username}' is not an owner of product '{product.productName}'")


def _validate_user_is_seller():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != RoleEnum.seller:
        abort(403,
              description="User bust be a seller to be able to edit products")


def _load_product(schema, *args, **kwargs):
    try:
        product = schema.load(*args, **kwargs)
    except ValueError as e:
        abort(400, str(e))
    return product


class ProductResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      summary: Get a product
      description: Get a single product by ID
      parameters:
        - in: path
          name: product_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  product: ProductSchema
        404:
          description: product does not exists
    put:
      tags:
        - api
      summary: Update a product
      description: Update a single product by ID
      parameters:
        - in: path
          name: product_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              ProductSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: product updated
                  product: ProductSchema
        404:
          description: product does not exists
    delete:
      tags:
        - api
      summary: Delete a product
      description: Delete a single product by ID
      parameters:
        - in: path
          name: product_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: product deleted
        404:
          description: product does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, product_id):
        schema = ProductSchema()
        product = Product.query.get_or_404(product_id)
        return {"product": schema.dump(product)}


    def put(self, product_id):
        _validate_user_is_seller()
        product = Product.query.get_or_404(product_id)
        _validate_user_is_owner(product)
        schema = ProductSchema(partial=True)
        product = _load_product(schema, request.json, instance=product)

        db.session.commit()

        return {"msg": "product updated", "product": schema.dump(product)}

    def delete(self, product_id):
        _validate_user_is_seller()
        product = Product.query.get_or_404(product_id)
        _validate_user_is_owner(product)
        db.session.delete(product)
        db.session.commit()

        return {"msg": "product deleted"}


class ProductList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      summary: Get a list of products
      description: Get a list of paginated products
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/ProductSchema'
    post:
      tags:
        - api
      summary: Create a product
      description: Create a new product
      requestBody:
        content:
          application/json:
            schema:
              ProductSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: product created
                  product: ProductSchema
    """

    @jwt_required()
    def get(self):
        schema = ProductSchema(many=True)
        query = Product.query
        return paginate(query, schema)

    @jwt_required()
    def post(self):
        schema = ProductSchema()
        _validate_user_is_seller()
        product = _load_product(schema, request.json)
        product.user_id = get_jwt_identity()
        db.session.add(product)
        db.session.commit()

        return {"msg": "product created", "product": schema.dump(product)}, 201
