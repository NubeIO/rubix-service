import datetime
import re
from typing import Dict

import jwt
from flask import current_app, request
from flask_restful import abort
from werkzeug.security import generate_password_hash

from src.setting import AppSetting
from src.system.utils.file import read_file, write_file


class UserModel:
    @classmethod
    def create_user(cls, username='admin', password='admin'):
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        existing_users = read_file(app_setting.users_file).split()
        if not existing_users:
            UserModel.update_user(username, password)

    @classmethod
    def update_user(cls, username, password):
        if not re.match("^([A-Za-z0-9_-])+$", username):
            raise ValueError("username should be alphanumeric and can contain '_', '-'")
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        hashed_password = generate_password_hash(password, method='sha256')
        default_user = f'{username}:{hashed_password}'
        write_file(app_setting.users_file, default_user)

    @classmethod
    def get_user(cls) -> Dict:
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        user = read_file(app_setting.users_file).split(":")
        if len(user) >= 2:
            return {
                'username': user[0],
                'password': user[1]
            }
        return {}

    @staticmethod
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

    @staticmethod
    def decode_jwt_token(token):
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        return jwt.decode(token, app_setting.secret_key, algorithms="HS256")

    @staticmethod
    def authorize():
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        if request.endpoint != 'users.login' and app_setting.auth:
            if 'Authorization' not in request.headers:
                abort(401, message='Authorization header is missing')

            data = request.headers['Authorization']
            access_token = str.replace(str(data), 'Bearer ', '')
            try:
                UserModel.decode_jwt_token(access_token)
            except Exception as e:
                abort(401, message=str(e))
