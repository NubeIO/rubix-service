#!/usr/bin/env python3

import multiprocessing
import os
from abc import ABC

import click
from gunicorn.app.base import Application
from gunicorn.glogging import Logger
from gunicorn.workers.ggevent import GeventWorker

from src import create_app, AppSetting
from src.envs import TOKEN_ENV, DATA_DIR_ENV, ARTIFACT_DIR_ENV, GLOBAL_DATA_DIR_ENV

CLI_CTX_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


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


@click.command(context_settings=CLI_CTX_SETTINGS)
@click.option('-p', '--port', type=int, default=1616, show_default=True, help='Port')
@click.option('-d', '--data-dir', type=click.Path(), default=lambda: os.environ.get(DATA_DIR_ENV),
              help='Application data dir')
@click.option('-g', '--global-dir', type=click.Path(), default=lambda: os.environ.get(GLOBAL_DATA_DIR_ENV),
              help='Global data dir')
@click.option('-a', '--artifact-dir', type=click.Path(), default=lambda: os.environ.get(ARTIFACT_DIR_ENV),
              help='Artifact downloaded dir')
@click.option('--token', type=str, default=lambda: os.environ.get(TOKEN_ENV),
              help='Service token to download from GitHub private repository')
@click.option('--prod', is_flag=True, help='Production mode')
@click.option('-s', '--setting-file', help='Rubix-Service: setting file')
@click.option('--workers', type=int, default=lambda: number_of_workers(),
              help='Gunicorn: The number of worker processes for handling requests.')
@click.option('-c', '--gunicorn-config', help='Gunicorn: config file(gunicorn.conf.py)')
@click.option('--log-level', type=click.Choice(['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], case_sensitive=False),
              show_default=True, help='Logging level')
def cli(port, data_dir, global_dir, artifact_dir, token, prod, workers, setting_file, gunicorn_config, log_level):
    setting = AppSetting(global_dir=global_dir, data_dir=data_dir, artifact_dir=artifact_dir, token=token,
                         prod=prod).reload(setting_file)
    options = {
        'bind': '%s:%s' % ('0.0.0.0', port),
        'workers': workers if prod else 1,
        'worker_class': GeventWorker.__module__ + '.' + GeventWorker.__qualname__,
        'logger_class': Logger.__module__ + '.' + Logger.__name__,
        'log_level': ('INFO' if prod else 'DEBUG' if log_level is None else log_level).lower(),
        'preload_app': True,
        'config': gunicorn_config
    }
    GunicornFlaskApplication(create_app(setting), options).run()


if __name__ == '__main__':
    cli()
