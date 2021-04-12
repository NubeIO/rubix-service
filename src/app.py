import logging
import os

from flask import Flask, request
from flask_cors import CORS

from .setting import AppSetting


def create_app(app_setting: AppSetting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')
    app = Flask(__name__)
    app_setting.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    cors = CORS()
    cors.init_app(app)

    def setup(self):
        with self.app_context():
            gunicorn_logger = logging.getLogger('gunicorn.error')
            app.logger.handlers = gunicorn_logger.handlers
            app.logger.setLevel(gunicorn_logger.level)

    @app.before_first_request
    def create_default_user():
        from src.users.model_users import UserModel
        UserModel.create_user()

    @app.before_request
    def before_request_fn():
        env: dict = request.environ
        if not (env.get('REMOTE_ADDR', '') == "127.0.0.1" and "python-requests" in env.get('HTTP_USER_AGENT', '')):
            from src.users.model_users import UserModel
            UserModel.authorize()

    def register_router(_app: Flask) -> Flask:
        from src.routes import bp_system, bp_networking, bp_service, bp_app, bp_wires, bp_users, bp_gw_mqtt, bp_discover
        from src.proxy.reverse_proxy_routes import bp_reverse_proxy

        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_networking)
        _app.register_blueprint(bp_service)
        _app.register_blueprint(bp_app)
        _app.register_blueprint(bp_wires)
        _app.register_blueprint(bp_reverse_proxy)
        _app.register_blueprint(bp_users)
        _app.register_blueprint(bp_gw_mqtt)

        if app_setting.mqtt_rest_bridge_setting.enabled and app_setting.mqtt_rest_bridge_setting.master:
            from src.proxy.master_proxy_routes import bp_master_proxy
            from src.proxy.slave_proxy_routes import bp_slave_proxy
            from src.proxy.slaves_multicast_proxy_routes import bp_slaves_multicast_proxy
            from src.proxy.slaves_broadcast_proxy_routes import bp_slaves_broadcast_proxy
            _app.register_blueprint(bp_discover)
            _app.register_blueprint(bp_master_proxy)
            _app.register_blueprint(bp_slave_proxy)
            _app.register_blueprint(bp_slaves_broadcast_proxy)
            _app.register_blueprint(bp_slaves_multicast_proxy)
        return _app

    setup(app)
    return register_router(app)
