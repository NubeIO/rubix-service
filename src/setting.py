import os
import secrets

from flask import Flask

from src.system.utils.file import write_file, read_file


class AppSetting:
    PORT = 1616
    GLOBAL_DIR_ENV = 'GLOBAL_DIR'
    DATA_DIR_ENV = 'RUBIX_SERVICE_DATA'
    CONFIG_DIR_ENV = 'RUBIX_SERVICE_CONFIG'
    ARTIFACT_DIR_ENV = 'ARTIFACT_DIR'
    BACKUP_DATA_DIR_ENV = 'BACKUP_DATA'
    FLASK_KEY: str = 'APP_SETTING'

    default_global_dir: str = 'out'
    default_data_dir: str = 'data'
    default_config_dir: str = 'config'
    default_artifact_dir: str = 'apps'
    default_backup_dir: str = 'backup'
    default_secret_key_file = 'secret_key.txt'
    default_token_file = 'token.txt'
    default_logging_conf: str = 'logging.conf'
    fallback_logging_conf: str = 'config/logging.example.conf'
    fallback_prod_logging_conf: str = 'config/logging.prod.example.conf'
    default_users_file = 'users.txt'

    def __init__(self, **kwargs):
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), self.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('data_dir')),
                                             self.__join_global_dir(self.default_data_dir))
        self.__config_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('config_dir')),
                                               self.__join_global_dir(self.default_config_dir))
        self.__artifact_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('artifact_dir')),
                                                 self.__join_global_dir(self.default_artifact_dir))
        self.__backup_dir = self.__compute_dir(kwargs.get('backup_dir'), self.default_backup_dir, 0o777)
        self.__download_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'download'))
        self.__install_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'install'))
        self.__token_file = os.path.join(self.__data_dir, self.default_token_file)
        self.__prod = kwargs.get('prod') or False
        self.__device_type = kwargs.get('device_type')
        self.__secret_key = ''
        self.__secret_key_file = os.path.join(self.__config_dir, self.default_secret_key_file)
        self.__users_file = os.path.join(self.__data_dir, self.default_users_file)
        self.__auth = kwargs.get('auth') or False

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def config_dir(self):
        return self.__config_dir

    @property
    def artifact_dir(self) -> str:
        return self.__artifact_dir

    @property
    def backup_dir(self):
        return self.__backup_dir

    @property
    def download_dir(self) -> str:
        return self.__download_dir

    @property
    def install_dir(self) -> str:
        return self.__install_dir

    @property
    def token(self) -> str:
        return read_file(os.path.join(self.data_dir, self.default_token_file))

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

    @property
    def users_file(self) -> str:
        return self.__users_file

    def reload(self, setting_file: str):
        return self

    def init_app(self, app: Flask):
        self.__secret_key = AppSetting.__handle_secret_key(self.__secret_key_file)
        app.config[AppSetting.FLASK_KEY] = self
        return self

    def __join_global_dir(self, _dir):
        return _dir if _dir is None or _dir.strip() == '' else os.path.join(self.__global_dir, _dir)

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

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
