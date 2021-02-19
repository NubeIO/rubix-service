from flask_restful import Resource, reqparse, marshal_with, abort, fields

from src.users.model_users import UserModel


class UsersResource(Resource):
    return_fields = {
        'username': fields.String
    }

    @classmethod
    @marshal_with(return_fields)
    def get(cls):
        user = UserModel.get_user()
        if not user:
            abort(404, message='Users not found')
        return user

    @classmethod
    @marshal_with(return_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        try:
            UserModel.update_user(data['username'], data['password'])
            return UserModel.get_user()
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
