import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserResgister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required = True, help = "this field cannot be left blank")
    parser.add_argument('password', type = str, required = True, help = "this field cannot be left blank")

    def post(self):
        data = UserResgister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message' : "user '{}' already exists".format(data['username'])}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message' : 'user created'}, 201
