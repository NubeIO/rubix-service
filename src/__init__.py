import os
import logging

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from src.system.utils.auth import get_auth_file
from src.system.utils.file import delete_file, write_file

db = SQLAlchemy()
cors = CORS()


def create_app(data_dir, token: str, prod: bool, setting_file: str) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if prod else 'development')
    __handle_token(data_dir, token)

    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{data_dir}/data.db?timeout=60'
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
        _app.register_blueprint(bp_ping)
        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_service)
        _app.register_blueprint(bp_app)
        _app.register_blueprint(bp_wires)
        return _app

    return register_router(app)


def __handle_token(data_dir, token):
    auth_file = get_auth_file(data_dir)
    if token:
        write_file(auth_file, token)
    else:
        delete_file(auth_file)
