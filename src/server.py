from abc import ABC

from gunicorn.app.base import BaseApplication
from gunicorn.arbiter import Arbiter

from .app import create_app
from .setting import AppSetting


class GunicornFlaskApplication(BaseApplication, ABC):

    def __init__(self, _app_setting: AppSetting, _options=None):
        self._options = _options or {}
        self._options.update({'when_ready': when_ready, 'on_exit': on_exit})
        super(GunicornFlaskApplication, self).__init__()
        self._app_setting = _app_setting
        self.application = None

    def load_config(self):
        config = {key: value for key, value in self._options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        self.application = create_app(self._app_setting)
        return self.application


def on_exit(server: Arbiter):
    server.log.info('Server is stopped')


def when_ready(server: Arbiter):
    server.log.info("Server is ready. Spawning workers...")
    server.app.application.setup()
