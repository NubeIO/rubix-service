import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.lora_raw_app import LoRaRawApp
from src.system.utils.file import delete_file, write_file, read_file

db = SQLAlchemy()
cors = CORS()


class AppSetting:
    _token_file_name = 'auth.txt'
    _global_dir = 'out'
    _data_dir = 'rubix-service'
    _artifact_dir = 'apps'
    _token = ''
    _prod = False
    _token_file = 'auth.txt'

    def __init__(self, **kwargs):
        self._global_dir = self.__compute_dir(kwargs['global_dir'], self._global_dir, 0o777)
        self._data_dir = self.__compute_dir(kwargs['data_dir'], os.path.join(self._global_dir, self._data_dir))
        self._artifact_dir = self.__compute_dir(kwargs['artifact_dir'],
                                                os.path.join(self._data_dir, self._artifact_dir))
        self._token = None if kwargs['token'] is None or kwargs['token'].strip() == '' else kwargs['token']
        self._token_file = os.path.join(self._data_dir, self._token_file_name)
        self._prod = kwargs['prod']

    @property
    def global_dir(self):
        return self._global_dir

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def artifact_dir(self) -> str:
        return self._artifact_dir

    @property
    def token(self) -> str:
        return self._token

    @property
    def prod(self) -> bool:
        return self._prod

    def reload(self, setting_file: str):
        return self

    def init_app(self, app: Flask):
        self._token = AppSetting.__handle_token(self._token_file, self._token)
        app.config['SETTING'] = self
        return self

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __handle_token(token_file, token) -> str:
        if token:
            write_file(token_file, token)
            return token
        else:
            return read_file(token_file, debug=True)


def create_app(app_setting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')

    app = Flask(__name__)
    app_setting = app_setting.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/data.db?timeout=60'.format(app_setting.data_dir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    cors.init_app(app)
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def register_router(_app) -> Flask:
        from src.routes import bp_ping
        from src.routes import bp_system
        from src.routes import bp_service
        from src.routes import bp_app
        from src.routes import bp_wires
        from src.reverse_proxy_routes import bp_reverse_proxy

        _app.register_blueprint(bp_ping)
        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_service)
        _app.register_blueprint(bp_app)
        _app.register_blueprint(bp_wires)
        _app.register_blueprint(bp_reverse_proxy)
        return _app

    return register_router(app)
