import os

from flask import Flask

from src.system.utils.file import write_file


class AppSetting:
    TOKEN_ENV = 'RUBIX_SERVICE_TOKEN'
    DATA_DIR_ENV = 'RUBIX_SERVICE_DATA'
    ARTIFACT_DIR_ENV = 'ARTIFACT_DIR'
    GLOBAL_DATA_DIR_ENV = 'GLOBAL_DATA'
    KEY: str = 'APP_SETTING'

    default_global_dir: str = 'out'
    default_data_dir: str = 'rubix-service'
    default_artifact_dir: str = 'apps'
    default_token_file = 'auth.txt'

    def __init__(self, **kwargs):
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), self.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(kwargs.get('data_dir'),
                                             os.path.join(self.global_dir, self.default_data_dir))
        self.__artifact_dir = self.__compute_dir(kwargs.get('artifact_dir'),
                                                 os.path.join(self.data_dir, self.default_artifact_dir))
        self.__token = '' if not kwargs.get('token') else kwargs.get('token')
        self.__token_file = os.path.join(self.data_dir, self.default_token_file)
        self.__prod = kwargs.get('prod') or False

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
    def token(self) -> str:
        return self.__token

    @property
    def prod(self) -> bool:
        return self.__prod

    def reload(self, setting_file: str):
        return self

    def init_app(self, app: Flask):
        AppSetting.__handle_token(self.__token_file, self.__token)
        app.config[AppSetting.KEY] = self
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
