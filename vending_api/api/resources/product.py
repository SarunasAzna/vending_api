from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from vending_api.api.schemas import ProductSchema
from vending_api.commons.pagination import paginate
from vending_api.extensions import db
from vending_api.models import Product


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


    def get(self, product_id):
        schema = ProductSchema()
        product = Product.query.get_or_404(product_id)
        return {"product": schema.dump(product)}

    @jwt_required()
    def put(self, product_id):
        schema = ProductSchema(partial=True)
        product = Product.query.get_or_404(product_id)
        product = schema.load(request.json, instance=product)

        db.session.commit()

        return {"msg": "product updated", "product": schema.dump(product)}

    #@jwt_required()
    #def delete(self, product_id):
    #    product = Product.query.get_or_404(product_id)
    #    db.session.delete(product)
    #    db.session.commit()

    #    return {"msg": "product deleted"}


#class UserList(Resource):
#    """Creation and get_all
#
#    ---
#    get:
#      tags:
#        - api
#      summary: Get a list of users
#      description: Get a list of paginated users
#      responses:
#        200:
#          content:
#            application/json:
#              schema:
#                allOf:
#                  - $ref: '#/components/schemas/PaginatedResult'
#                  - type: object
#                    properties:
#                      results:
#                        type: array
#                        items:
#                          $ref: '#/components/schemas/UserSchema'
#    post:
#      tags:
#        - api
#      summary: Create a user
#      description: Create a new user
#      requestBody:
#        content:
#          application/json:
#            schema:
#              UserSchema
#      responses:
#        201:
#          content:
#            application/json:
#              schema:
#                type: object
#                properties:
#                  msg:
#                    type: string
#                    example: user created
#                  user: UserSchema
#    """
#
#    @jwt_required()
#    def get(self):
#        schema = UserSchema(many=True)
#        query = User.query
#        return paginate(query, schema)
#
#    def post(self):
#        schema = UserSchema()
#        user = schema.load(request.json)
#
#        db.session.add(user)
#        db.session.commit()
#
#        return {"msg": "user created", "user": schema.dump(user)}, 201
