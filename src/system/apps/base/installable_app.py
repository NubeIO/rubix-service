import json
import os
import shutil
from abc import abstractmethod, ABC
from datetime import datetime

import requests
from flask import current_app
from packaging import version as packaging_version
from werkzeug.datastructures import FileStorage
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import get_instance
from src.model import BaseModel
from src.setting import InstallableAppSetting
from src.system.apps.enums.types import Types
from src.system.utils.file import delete_existing_folder, download_unzip_service, is_dir_exist, upload_unzip_service, \
    write_file, delete_file, directory_zip_service
from src.system.utils.shell import execute_command

logger = LocalProxy(lambda: current_app.logger)


class InstallableApp(BaseModel, ABC):

    def __init__(self):
        self.__version = ''
        self.__app_setting: InstallableAppSetting = InstallableAppSetting()

    @classmethod
    def get_app(cls, service, version):
        app_settings = current_app.config[AppSetting.FLASK_KEY].installable_app_settings
        setting = next((item for item in app_settings if item.service == service), None)
        if setting is None:
            raise ModuleNotFoundError(f"service {service} does not exist in our system")
        instance = get_instance(InstallableApp, setting.app_type)
        if instance is not None:
            instance.__version = version
            instance.__app_setting = setting
            return instance
        raise ModuleNotFoundError(f"app_type {setting.app_type} does not exist in our system")

    @property
    def service(self) -> str:
        """service for mapping frontend request with the App"""
        return self.__app_setting.service

    @property
    def display_name(self):
        """display_name for frontend side"""
        return self.__app_setting.display_name

    @property
    def repo_name(self):
        """name for installation folder creation and github repo name validation"""
        return self.__app_setting.repo_name

    @property
    def service_file_name(self):
        """service_file_name for systemd name"""
        return self.__app_setting.service_file_name

    @property
    def pre_start_sleep(self):
        """pre_start_sleep for pausing process"""
        return self.__app_setting.pre_start_sleep

    @property
    def data_dir_name(self):
        """data_dir_name for making/denoting a valid data dir"""
        return self.__app_setting.data_dir_name

    @property
    def port(self):
        """port for running app"""
        return self.__app_setting.port

    @property
    def min_support_version(self):
        return self.__app_setting.min_support_version

    @property
    def description(self):
        """description for systemd"""
        return self.__app_setting.description

    @property
    def app_type(self):
        """type of app"""
        return ""

    @property
    def gateway_access(self):
        return self.__app_setting.gateway_access

    @property
    def url_prefix(self):
        """url_prefix for running app"""
        return self.__app_setting.url_prefix

    @property
    def version(self):
        return self.__version

    @property
    def need_wires_plat(self):
        return self.__app_setting.need_wires_plat

    @property
    def is_asset(self):
        """Accept: "application/octet-stream" needs to be added on headers if it is downloading from assets list"""
        return True

    @property
    def app_setting(self):
        return self.__app_setting

    @abstractmethod
    def select_link(self, row: any, is_browser_downloadable: bool):
        """select_link for selecting builds from GitHub"""
        raise NotImplementedError("select_link needs to be overridden")

    def download(self) -> dict:
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        download_name = download_unzip_service(self.get_download_link(app_setting.token), self.get_download_dir()
                                               , app_setting.token, self.is_asset)
        existing_app_deletion: bool = delete_existing_folder(self.get_downloaded_dir())
        self.after_download_upload(download_name)
        return {'service': self.service, 'version': self.version, 'existing_app_deletion': existing_app_deletion}

    def download_async(self, app_context):
        if app_context:
            with app_context():
                try:
                    return self.download()
                except Exception as e:
                    return {'service': self.service(), 'version': self.version, 'error': str(e)}

    def upload(self, file: FileStorage) -> dict:
        upload_name = upload_unzip_service(file, self.get_download_dir())
        existing_app_deletion: bool = delete_existing_folder(self.get_downloaded_dir())
        self.after_download_upload(upload_name)
        return {'service': self.service, 'version': self.version, 'existing_app_deletion': existing_app_deletion}

    def update_config_file(self, data: str) -> bool:
        if self.app_type == Types.PYTHON_APP.value:
            write_file(os.path.join(self.get_global_dir(), 'config/config.json'), data)
            return True
        return False

    def update_logging_file(self, data: str) -> bool:
        if self.app_type == Types.PYTHON_APP.value:
            write_file(os.path.join(self.get_global_dir(), 'config/logging.conf'), data)
            return True
        return False

    def update_env_file(self, data: str) -> bool:
        if self.app_type == Types.FRONTEND_APP.value:
            write_file(os.path.join(self.get_global_dir(), 'config/.env'), data)
            return True
        return False

    def delete_config_file(self) -> bool:
        if self.app_type == Types.PYTHON_APP.value:
            delete_file(os.path.join(self.get_global_dir(), 'config/config.json'))
            return True
        return False

    def delete_logging_file(self) -> bool:
        if self.app_type == Types.PYTHON_APP.value:
            delete_file(os.path.join(self.get_global_dir(), 'config/logging.conf'))
            return True
        return False

    def delete_env_file(self) -> bool:
        if self.app_type == Types.FRONTEND_APP.value:
            delete_file(os.path.join(self.get_global_dir(), 'config/.env'))
            return True
        return False

    def after_download_upload(self, name: str):
        # they are already wrapped on folder
        download_dir: str = self.get_download_dir()
        extracted_dir = os.path.join(download_dir, name)
        os.rename(extracted_dir, self.get_downloaded_dir())

    @abstractmethod
    def install(self) -> bool:
        raise NotImplementedError("install needs to be overridden")

    @abstractmethod
    def uninstall(self) -> bool:
        raise NotImplementedError("uninstall needs to be overridden")

    def stop(self) -> bool:
        logger.info('Stopping Linux Service...')
        if not execute_command('sudo systemctl stop {}'.format(self.service_file_name)):
            return False
        logger.info('Successfully stopped service.')
        return True

    def restart(self) -> bool:
        logger.info('Restarting Linux Service...')
        if not execute_command(f'sudo systemctl restart {self.service_file_name}'):
            return False
        logger.info('Successfully restarted service.')
        return True

    def backup_data(self):
        logger.info('Starting data backup...')
        global_dir = self.get_global_dir()
        if is_dir_exist(global_dir):
            shutil.copytree(global_dir, self.get_backup_dir())
            logger.info('Successfully completed data backup...')
            return True
        return False

    def download_data(self):
        return directory_zip_service(os.path.join(self.get_global_dir(), 'data'))

    def get_global_dir(self) -> str:
        setting = current_app.config[AppSetting.FLASK_KEY]
        return os.path.join(setting.root_dir, self.data_dir_name)

    def get_releases_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/releases'.format(self.repo_name)

    def get_download_link(self, token: str, is_browser_downloadable: bool = False):
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        release_link: str = f'https://api.github.com/repos/NubeIO/{self.repo_name}/releases/tags/{self.version}'
        resp = requests.get(release_link, headers=headers)
        row: str = json.loads(resp.content)
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        download_link = self.select_link(row, is_browser_downloadable)
        if not download_link:
            raise ModuleNotFoundError(
                f'No app for type {setting.device_type} & version {self.version}, check your token & repo')
        return download_link

    def get_latest_release(self, token: str):
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        release_link: str = f'https://api.github.com/repos/NubeIO/{self.repo_name}/releases'
        resp = requests.get(release_link, headers=headers)
        data = json.loads(resp.content)
        latest_release = ''
        for row in data:
            release = row.get('tag_name', '') if type(row) is dict else ''
            if not latest_release or packaging_version.parse(latest_release) <= packaging_version.parse(release):
                latest_release = release
        if not latest_release:
            raise ModuleNotFoundError('No version found, check your token & repo')
        return latest_release

    def get_cwd(self) -> str:
        """current working dir for script.bash execution"""
        return self.get_installed_dir()

    def get_wd(self) -> str:
        """working dir for systemd working directory set"""
        return self.get_installed_dir()

    def get_download_dir(self) -> str:
        setting = current_app.config[AppSetting.FLASK_KEY]
        return os.path.join(setting.download_dir, self.repo_name)

    def get_installation_dir(self) -> str:
        setting = current_app.config[AppSetting.FLASK_KEY]
        return os.path.join(setting.install_dir, self.repo_name)

    def get_downloaded_dir(self):
        return os.path.join(self.get_download_dir(), self.version)

    def get_installed_dir(self):
        return os.path.join(self.get_installation_dir(), self.version)

    def get_backup_dir(self):
        setting = current_app.config[AppSetting.FLASK_KEY]
        return os.path.join(setting.backup_dir, self.repo_name,
                            f'{datetime.now().strftime("%Y%m%d%H%M%S")}_{self.version}')

    def set_version(self, _version):
        self.__version = _version

    def set_app_settings(self, _app_Settings):
        self.__app_setting = _app_Settings
