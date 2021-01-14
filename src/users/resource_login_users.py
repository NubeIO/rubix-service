import jwt
import datetime
from flask import current_app
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from werkzeug.security import generate_password_hash, check_password_hash

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
        user = UsersModel.query.filter_by(user_name=data['user_name']).first()

        if user and check_password_hash(user.password, data['password']):
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user.user_name
            }
            encoded = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            return {'access_token': encoded, 'token_type': 'JWT'}
        else:
            if not user:
                abort(404, message='User not found')
            else:
                abort(404, message='Invalid password')
