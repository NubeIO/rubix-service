import multiprocessing
from abc import ABC

from gunicorn.app.base import Application
import gunicorn
from gunicorn import glogging
from gunicorn.workers import sync

from src import app


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class GunicornFlaskApplication(Application, ABC):

    def __init__(self, _app, _options=None):
        self.options = _options or {}
        self.application = _app
        super(GunicornFlaskApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '1616'),
        'workers': 1,
        'preload_app': True
    }
    GunicornFlaskApplication(app, options).run()
