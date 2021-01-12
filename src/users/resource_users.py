from flask_restful import Resource, reqparse, marshal_with, abort
from werkzeug.security import generate_password_hash

from src.users.model_users import UsersModel
from src.users.schema_users import users_all_attributes, users_all_fields


class UsersResource(Resource):
    parser = reqparse.RequestParser()
    for attr in users_all_attributes:
        parser.add_argument(attr,
                            type=users_all_attributes[attr]['type'],
                            required=users_all_attributes[attr].get('required', False),
                            help=users_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(users_all_fields)
    def get(cls):
        users = UsersModel.query.all()
        if len(users) > 0:
            abort(404, message='Users not found')
        return users

    @classmethod
    @marshal_with(users_all_fields)
    def put(cls):
        data = UsersResource.parser.parse_args()
        print(data['password'])
        data['password'] = generate_password_hash(data['password'])
        user = UsersModel.query.first()
        try:
            if not user:
                abort(404, message='User is invalid')
            else:
                user.update(**{**data, "uuid": user.uuid})
                return UsersModel.find_by_uuid(user.uuid)
        except Exception as e:
            abort(500, message=str(e))
