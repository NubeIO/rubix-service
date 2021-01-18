import datetime
import uuid

import jwt
from flask import current_app, request
from flask_restful import abort
from werkzeug.security import generate_password_hash

from src import db, AppSetting
from src.platform.model_base import ModelBase


class UsersModel(ModelBase):
    __tablename__ = 'users'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "Users({})".format(self.uuid)

    @classmethod
    def find_by_username(cls, user_uuid):
        return cls.query.filter_by(uuid=user_uuid).first()

    @classmethod
    def create_user(cls, username='admin', password='admin'):
        if not UsersModel.query.first():
            hashed_password = generate_password_hash(password, method='sha256')
            _uuid = str(uuid.uuid4())
            default_user = UsersModel(uuid=_uuid, username=username, password=hashed_password)
            db.session.add(default_user)
            db.session.commit()

    @staticmethod
    def encode_jwt_token(username):
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=0, seconds=0),
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
                UsersModel.decode_jwt_token(access_token)
            except Exception as e:
                abort(401, message=str(e))
