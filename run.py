#!/usr/bin/env python3

import multiprocessing
import os

import click

from src import AppSetting, GunicornFlaskApplication
from src.system.systemd.systemd import RubixServiceSystemdCreator

CLI_CTX_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


@click.command(context_settings=CLI_CTX_SETTINGS)
@click.option('-p', '--port', type=int, default=1616, show_default=True, help='Port')
@click.option('-d', '--data-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.DATA_DIR_ENV),
              help='Application data dir')
@click.option('-g', '--global-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.GLOBAL_DATA_DIR_ENV),
              help='Global data dir')
@click.option('-a', '--artifact-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.ARTIFACT_DIR_ENV),
              help='Artifact downloaded dir')
@click.option('--token', type=str, default=lambda: os.environ.get(AppSetting.TOKEN_ENV),
              help='Service token to download from GitHub private repository')
@click.option('--prod', is_flag=True, help='Production mode')
@click.option('-s', '--setting-file', help='Rubix-Service: setting json file')
@click.option('--workers', type=int, default=lambda: number_of_workers(),
              help='Gunicorn: The number of worker processes for handling requests.')
@click.option('-c', '--gunicorn-config', help='Gunicorn: config file(gunicorn.conf.py)')
@click.option('--log-level', type=click.Choice(['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], case_sensitive=False),
              show_default=True, help='Logging level')
@click.option('--create', is_flag=True, help='Create auto-restart systemd file')
def cli(port, data_dir, global_dir, artifact_dir, token, prod, workers, setting_file, gunicorn_config, log_level,
        create):
    setting = AppSetting(global_dir=global_dir, data_dir=data_dir, artifact_dir=artifact_dir, token=token,
                         prod=prod).reload(setting_file)

    if create:
        creator = RubixServiceSystemdCreator(os.getcwd(), port, setting.data_dir, setting.global_dir,
                                             setting.artifact_dir, setting.token)
        creator.create_and_start_service()
    else:
        options = {
            'bind': '%s:%s' % ('0.0.0.0', port),
            'workers': workers if prod else 1,
            'log_level': ('INFO' if prod else 'DEBUG' if log_level is None else log_level).lower(),
            'preload_app': True,
            'config': gunicorn_config
        }
        GunicornFlaskApplication(setting, options).run()


if __name__ == '__main__':
    cli()
