from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource
from werkzeug.security import check_password_hash

from src.users.model_users import UserModel


class UsersLoginResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        user = UserModel.get_user()
        if user and user['username'] == data['username'] and check_password_hash(user['password'], data['password']):
            return UserModel.encode_jwt_token(user['username'])
        else:
            raise NotFoundException('username and password combination is incorrect')
