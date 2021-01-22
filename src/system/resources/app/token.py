import os

from flask import current_app
from flask_restful import Resource, reqparse

from src.setting import AppSetting
from src.system.utils.file import write_file


class TokenResource(Resource):

    @classmethod
    def put(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        data_dir: str = app_setting.data_dir
        token_file = os.path.join(data_dir, AppSetting.default_token_file)

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        token = args['token']
        write_file(token_file, '' if not token else token)
        return {
            'token': token
        }
