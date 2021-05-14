import datetime
import re
from distutils.util import strtobool

import jwt
from flask import current_app, request
from flask_restful import fields, abort
from flask_restful import marshal
from rubix_http.exceptions.exception import BadDataException, NotFoundException
from werkzeug.security import generate_password_hash

from src import AppSetting


def model_marshaller_with_children(data: any, args: dict, base_fields: dict, children_fields: dict):
    with_children = False
    if 'with_children' in args:
        try:
            with_children = bool(strtobool(args['with_children']))
        except Exception:
            raise BadDataException('Invalid query string')

    if with_children:
        return marshal(data, children_fields)
    else:
        return marshal(data, base_fields)


def get_field_type(attr_type):
    if attr_type == int:
        return fields.Integer()
    elif attr_type == str:
        return fields.String()
    elif attr_type == bool:
        return fields.Boolean()
    elif attr_type == float:
        return fields.Float()


def map_rest_schema(schema, resource_fields):
    """
    Adds schema dict marshaled data to resource_fields dict
    """
    for attr in schema:
        # hack fix... change to make fields primary thing and switch get_field_type to return opposite
        if not isinstance(schema[attr]['type'], fields.Raw):
            resource_fields[attr] = get_field_type(schema[attr]['type'])
        else:
            resource_fields[attr] = schema[attr]['type']
        if schema[attr].get('nested', False):
            resource_fields[attr].__init__(attribute=schema[attr]['dict'])


def encode_jwt_token(username):
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, hours=0, seconds=0),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    encoded = jwt.encode(payload, app_setting.secret_key, algorithm='HS256')

    return {
        'access_token': encoded,
        'token_type': 'JWT'
    }


def decode_jwt_token(token):
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    return jwt.decode(token, app_setting.secret_key, algorithms="HS256")


def authorize():
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    if request.endpoint != 'users.login' and app_setting.auth:
        if request.endpoint != 'users.login' and app_setting.auth:
            if 'Authorization' not in request.headers:
                abort(401, message='Authorization header is missing')

            data = request.headers['Authorization']
            access_token = str.replace(str(data), 'Bearer ', '')
            try:
                decode_jwt_token(access_token)
            except Exception as e:
                abort(401, message=str(e))


def encrypt_password(password):
    error = ''
    if len(password) < 8:
        error = f'password must have at lease 8 characters.'
    if not re.search(r'[\d]+', password):
        error = f'{error} password must have at least one digit (0-9).'
    if not re.search('[A-Z]+', password):
        error = f'{error} password must have at least one uppercase (A-Z).'
    if error:
        raise ValueError(error)
    return generate_password_hash(password, method='sha256')
