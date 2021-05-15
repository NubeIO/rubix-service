import uuid as uuid_
from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource
from werkzeug.security import check_password_hash

from src.models.enum import StateType, RoleType
from src.models.user.model_user import UserModel
from src.resources.rest_schema.schema_user import user_all_attributes, user_return_fields, user_all_fields_with_children
from src.resources.utils import encode_jwt_token, encrypt_password, decode_jwt_token, get_access_token


class UserResourceList(RubixResource):
    parser = reqparse.RequestParser()
    for attr in user_all_attributes:
        parser.add_argument(attr,
                            type=user_all_attributes[attr]['type'],
                            required=user_all_attributes[attr].get('required', False),
                            help=user_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls):
        return UserModel.find_all()

    @classmethod
    @marshal_with(user_return_fields)
    def post(cls):
        args = cls.parser.parse_args()
        uuid = str(uuid_.uuid4())
        user = UserModel(uuid=uuid, **args)
        user.password = encrypt_password(user.password)
        user.save_to_db()
        return user


class UserResource(RubixResource):
    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls, **kwargs):
        user: UserModel = cls.get_user(**kwargs)
        if user is None:
            raise NotFoundException('User not found')
        return user

    @classmethod
    @marshal_with(user_return_fields)
    def patch(cls, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=False, store_missing=False)
        parser.add_argument('last_name', type=str, required=False, store_missing=False)
        parser.add_argument('email', type=str, required=False, store_missing=False)
        parser.add_argument('device_ids', type=str, required=False, store_missing=False)
        args = parser.parse_args()
        user: UserModel = cls.get_user(**kwargs)
        if user is None:
            raise NotFoundException("User not found")
        user.update(**args)
        return user

    @classmethod
    def delete(cls, **kwargs):
        user: UserModel = cls.get_user(**kwargs)
        user.delete_from_db()
        return {'message': 'User has been deleted successfully'}

    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        raise NotImplementedError


class UserResourceByUUID(UserResource):
    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        return UserModel.find_by_uuid(kwargs.get('uuid'))


class UserResourceByUsername(UserResource):
    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        return UserModel.find_by_username(kwargs.get('username'))


class UserVerifyResource(RubixResource):

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        user: UserModel = UserModel.find_by_username(args['username'])
        if user is None:
            raise NotFoundException("User not found")
        user.state = StateType.VERIFIED
        user.commit()
        return {'message': 'User has been verified successfully'}


class UserChangePasswordResource(RubixResource):

    @classmethod
    def post(cls):
        access_token = get_access_token()
        parser = reqparse.RequestParser()
        parser.add_argument('new_password', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        username = decode_jwt_token(access_token).get('username', '')
        user: UserModel = UserModel.find_by_username(username)
        if user is None:
            raise NotFoundException("User not found")
        user.password = encrypt_password(args['new_password'])
        user.commit()
        return {'message': 'Your password has been changed successfully'}


class UserLoginResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, store_missing=False)
        parser.add_argument('password', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        user = UserModel.find_by_username(args['username'])
        if user is None:
            raise NotFoundException('User not found')
        if user.state == StateType.UNVERIFIED:
            raise BadDataException('User is not verified')
        if not check_password_hash(user.password, args['password']):
            raise BadDataException('username and password combination is incorrect')
        return encode_jwt_token(user.uuid, user.username, user.role == RoleType.ADMIN)
