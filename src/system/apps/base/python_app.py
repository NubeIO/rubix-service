import os
from abc import ABC

from flask import current_app
from werkzeug.local import LocalProxy

from src import AppSetting
from src.pyinstaller import resource_path
from src.system.apps.base.systemd_app import SystemdApp
from src.system.apps.enums.types import Types

logger = LocalProxy(lambda: current_app.logger)


class PythonApp(SystemdApp, ABC):
    @property
    def app_type(self):
        return Types.PYTHON_APP.value

    def select_link(self, row: any, is_browser_downloadable: bool):
        setting = current_app.config[AppSetting.FLASK_KEY]
        for asset in row.get('assets', []):
            if setting.device_type in asset.get('name'):
                if is_browser_downloadable:
                    return {
                        'name': row.get('name'),
                        'created_at': row.get('created_at'),
                        'browser_download_url': asset.get('browser_download_url')
                    }
                return asset.get('url')

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

    def create_service(self):
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
