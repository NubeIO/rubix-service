import os
from abc import ABC

from flask import current_app
from werkzeug.local import LocalProxy

from src import AppSetting
from src.pyinstaller import resource_path
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types
from src.system.utils.file import delete_file
from src.system.utils.shell import execute_command

logger = LocalProxy(lambda: current_app.logger)

SERVICE_DIR = '/lib/systemd/system'
SERVICE_DIR_SOFT_LINK = '/etc/systemd/system/multi-user.target.wants'


class PythonApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.PYTHON_APP.value

    def select_asset(self, row: any):
        setting = current_app.config[AppSetting.FLASK_KEY]
        for asset in row.get('assets', []):
            if setting.device_type in asset.get('name'):
                return asset.get('url')

    @property
    def service_file(self) -> str:
        return os.path.join(SERVICE_DIR, self.service_file_name)

    @property
    def symlink_service_file(self):
        return os.path.join(SERVICE_DIR_SOFT_LINK, self.service_file_name)

    def after_download(self, download_name: str):
        # enforcing to extract on version directory
        download_dir: str = self.get_download_dir()
        extracted_dir = os.path.join(download_dir, download_name)
        dir_with_version = os.path.join(download_dir, self.version)
        mode = 0o744
        os.makedirs(dir_with_version, mode, True)
        app_file = os.path.join(dir_with_version, 'app')
        os.rename(extracted_dir, app_file)
        os.chmod(app_file, mode)

    def install(self) -> bool:
        logger.info('Creating Linux Service...')
        lines = self._create_service()
        with open(self.service_file, "w") as file:
            file.writelines(lines)

        logger.info('Soft Un-linking Linux Service...')
        try:
            os.unlink(self.symlink_service_file)
        except FileNotFoundError as e:
            logger.info(str(e))

        logger.info('Soft Linking Linux Service...')
        os.symlink(self.service_file, self.symlink_service_file)

        logger.info('Hitting daemon-reload...')
        if not execute_command('sudo systemctl daemon-reload'):
            return False

        logger.info('Enabling Linux Service...')
        if not execute_command('sudo systemctl enable {}'.format(self.service_file_name)):
            return False

        logger.info('Starting Linux Service...')
        if not execute_command('sudo systemctl restart {}'.format(self.service_file_name)):
            return False

        logger.info('Successfully started service')
        return True

    def uninstall(self) -> bool:
        logger.info('Stopping Linux Service...')
        if not execute_command('systemctl stop {}'.format(self.service_file_name)):
            return False

        logger.info('Un-linking Linux Service...')
        try:
            os.unlink(self.symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        logger.info('Removing Linux Service...')
        delete_file(self.service_file)

        logger.info('Hitting daemon-reload...')
        if not execute_command('sudo systemctl daemon-reload'):
            return False
        logger.info('Service is deleted.')
        return True

    def restart(self) -> bool:
        logger.info('Restarting Linux Service...')
        if not execute_command('sudo systemctl restart {}'.format(self.service_file_name)):
            return False
        logger.info('Successfully restarted service.')
        return True

    def _create_service(self):
        lines = []
        with open(resource_path('systemd/nubeio-app-service.service')) as systemd_file:
            wd: str = self.get_wd()
            data_dir: str = self.get_data_dir()
            for line in systemd_file.readlines():
                if '<pre_start_sleep>' in line:
                    line = line.replace('<pre_start_sleep>', str(self.pre_start_sleep))
                if '<working_dir>' in line and wd:
                    line = line.replace('<working_dir>', wd)
                if '<port>' in line and self.port:
                    line = line.replace('<port>', str(self.port))
                if '<data_dir>' in line and data_dir:
                    line = line.replace('<data_dir>', data_dir)
                if '<name>' in line and self.repo_name:
                    line = line.replace('<name>', self.repo_name)
                if '<description>' in line and self.description:
                    line = line.replace('<description>', self.description)
                lines.append(line)
        return lines
