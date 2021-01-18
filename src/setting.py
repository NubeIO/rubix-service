import os
import secrets

from flask import Flask

from src.system.utils.file import write_file, read_file


class AppSetting:
    PORT = 1616
    TOKEN_ENV = 'RUBIX_SERVICE_TOKEN'
    DATA_DIR_ENV = 'RUBIX_SERVICE_DATA'
    ARTIFACT_DIR_ENV = 'ARTIFACT_DIR'
    GLOBAL_DATA_DIR_ENV = 'GLOBAL_DATA'
    FLASK_KEY: str = 'APP_SETTING'

    default_global_dir: str = 'out'
    default_data_dir: str = 'rubix-service'
    default_artifact_dir: str = 'apps'
    default_token_file = 'auth.txt'
    default_secret_key_file = 'secret_key.txt'

    def __init__(self, **kwargs):
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), self.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(kwargs.get('data_dir'),
                                             os.path.join(self.global_dir, self.default_data_dir))
        self.__artifact_dir = self.__compute_dir(kwargs.get('artifact_dir'),
                                                 os.path.join(self.data_dir, self.default_artifact_dir))
        self.__download_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'download'))
        self.__install_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'install'))
        self.__token = '' if not kwargs.get('token') else kwargs.get('token')
        self.__token_file = os.path.join(self.data_dir, self.default_token_file)
        self.__prod = kwargs.get('prod') or False
        self.__device_type = kwargs.get('device_type')
        self.__secret_key = ''
        self.__secret_key_file = os.path.join(self.data_dir, self.default_secret_key_file)
        self.__auth = kwargs.get('auth') or False

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def artifact_dir(self) -> str:
        return self.__artifact_dir

    @property
    def download_dir(self) -> str:
        return self.__download_dir

    @property
    def install_dir(self) -> str:
        return self.__install_dir

    @property
    def token(self) -> str:
        return self.__token

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def device_type(self) -> bool:
        return self.__device_type

    @property
    def secret_key(self) -> str:
        return self.__secret_key

    @property
    def auth(self) -> bool:
        return self.__auth

    def reload(self, setting_file: str):
        return self

    def init_app(self, app: Flask):
        self.__token = AppSetting.__handle_token(self.__token_file, self.__token)
        self.__secret_key = AppSetting.__handle_secret_key(self.__secret_key_file)
        app.config[AppSetting.FLASK_KEY] = self
        return self

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __handle_token(token_file, token) -> str:
        write_file(token_file, token)
        return token

    @staticmethod
    def __handle_secret_key(secret_key_file) -> str:
        if AppSetting.auth:
            existing_secret_key = read_file(secret_key_file)
            if existing_secret_key.strip():
                return existing_secret_key

            secret_key = AppSetting.__create_secret_key()
            write_file(secret_key_file, secret_key)
            return secret_key
        return ''

    @staticmethod
    def __create_secret_key():
        return secrets.token_hex(24)
