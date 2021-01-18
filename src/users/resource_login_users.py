from flask_restful import Resource, reqparse, marshal_with, abort
from werkzeug.security import check_password_hash

from src.users.model_users import UsersModel
from src.users.schema_users import users_all_attributes, users_token_fields


class UsersLoginResource(Resource):
    parser = reqparse.RequestParser()
    for attr in users_all_attributes:
        parser.add_argument(attr,
                            type=users_all_attributes[attr]['type'],
                            required=users_all_attributes[attr].get('required', False),
                            help=users_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(users_token_fields)
    def post(cls):
        data = UsersLoginResource.parser.parse_args()
        user = UsersModel.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            return UsersModel.encode_jwt_token(user.username)
        else:
            abort(404, message='username and password combination is incorrect')
