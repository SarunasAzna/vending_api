from flask import abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import exc

from vending_api.api.schemas import UserSchema
from vending_api.commons.pagination import paginate
from vending_api.extensions import db
from vending_api.models import User


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      summary: Get a user
      description: Get a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      summary: Update a user
      description: Update a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      summary: Delete a user
      description: Delete a single user by ID
      parameters:
        - in: path
          name: user_id
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
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        self_id = get_jwt_identity()
        if self_id != user_id:
            abort(403, "You can change only your user data.")
        if "deposit" in request.json:
            abort(400, "deposit cannot be updated with this action")
        if "role" in request.json:
            abort(400, "Role cannot be changed")
        try:
            user = schema.load(request.json, instance=user)
            db.session.commit()
        except exc.IntegrityError:
            abort(400, "Something went wrong, try another username")
        except ValueError as e:
            abort(400, str(e))

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        self_id = get_jwt_identity()
        if self_id != user_id:
            abort(403, "You can delete only yourself.")
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      summary: Get a list of users
      description: Get a list of paginated users
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
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      summary: Create a user
      description: Create a new user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: myuser
                  required: true
                password:
                  type: string
                  example: P4$$w0rd!
                  required: true
                role:
                  type: string
                  example: buyer
                  required: true
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    @jwt_required()
    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        if "deposit" in request.json:
            abort(400, "deposit cannot be updated with this action")
        try:
            user = schema.load(request.json)
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            abort(400, "Something went wrong, try another username")
        except ValueError as e:
            abort(400, str(e))

        return {"msg": "user created", "user": schema.dump(user)}, 201
