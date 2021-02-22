from flask_restful import reqparse, marshal_with, fields
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.users.model_users import UserModel


class UsersResource(RubixResource):
    return_fields = {
        'username': fields.String
    }

    @classmethod
    @marshal_with(return_fields)
    def get(cls):
        user = UserModel.get_user()
        if not user:
            raise NotFoundException('Users not found')
        return user

    @classmethod
    @marshal_with(return_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        UserModel.update_user(data['username'], data['password'])
        return UserModel.get_user()
