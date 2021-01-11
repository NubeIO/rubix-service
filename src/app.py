import logging
import os
import uuid
from functools import partial
from werkzeug.security import generate_password_hash

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .setting import AppSetting

db = SQLAlchemy()


def create_app(app_setting: AppSetting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')
    app = Flask(__name__)
    app_setting = app_setting.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/data.db?timeout=60'.format(app_setting.data_dir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    cors = CORS()
    cors.init_app(app)
    db.init_app(app)

    def setup(self):
        with self.app_context():
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

    @app.before_first_request
    def create_default_user():
        from src.users.model_users import UsersModel
        if not UsersModel.query.first():
            hashed_password = generate_password_hash('admin', method='sha256')
            _uuid = str(uuid.uuid4())
            default_user = UsersModel(uuid=_uuid, user_name='admin', password=hashed_password)
            db.session.add(default_user)
            db.session.commit()

    def register_router(_app: Flask) -> Flask:
        from src.routes import bp_system, bp_service, bp_app, bp_wires
        from src.reverse_proxy_routes import bp_reverse_proxy

        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_service)
        _app.register_blueprint(bp_app)
        _app.register_blueprint(bp_wires)
        _app.register_blueprint(bp_reverse_proxy)
        return _app

    app.setup = partial(setup, app)
    return register_router(app)
