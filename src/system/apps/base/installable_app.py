import json
import os
import shutil
from abc import abstractmethod, ABC
from packaging import version as packaging_version
from datetime import datetime

import requests
from flask import current_app
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import inheritors
from src.model import BaseModel
from src.system.utils.file import delete_existing_folder, download_unzip_service, is_dir_exist
from src.system.utils.shell import execute_command

logger = LocalProxy(lambda: current_app.logger)


class InstallableApp(BaseModel, ABC):

    def __init__(self, display_name, repo_name, service_file_name, data_dir_name, port, min_support_version,
                 description='', gateway_access=False, url_prefix='', version=''):

        self.__display_name = display_name
        self.__repo_name = repo_name
        self.__service_file_name = service_file_name
        self.__data_dir_name = data_dir_name
        self.__port = port
        self.__min_support_version = min_support_version
        self.__description = description
        self.__gateway_access = gateway_access
        self.__url_prefix = url_prefix
        self.__version = version

    @classmethod
    def get_app(cls, service, version):
        for subclass in inheritors(InstallableApp):
            if subclass.service() == service:
                instance = subclass()
                instance.__version = version
                return instance
        raise ModuleNotFoundError("service {} does not exist in our system".format(service))

    @classmethod
    @abstractmethod
    def service(cls) -> str:
        """service for mapping frontend request with the App"""
        raise NotImplementedError("service needs to be overridden")

    @property
    def display_name(self):
        """display_name for frontend side"""
        return self.__display_name

    @property
    def repo_name(self):
        """name for installation folder creation and github repo name validation"""
        return self.__repo_name

    @property
    def service_file_name(self):
        """service_file_name for systemd name"""
        return self.__service_file_name

    @property
    def pre_start_sleep(self):
        """pre_start_sleep for pausing process"""
        return 0

    @property
    def data_dir_name(self):
        """data_dir_name for making/denoting a valid data dir"""
        return self.__data_dir_name

    @property
    def port(self):
        """port for running app"""
        return self.__port

    @property
    def min_support_version(self):
        return self.__min_support_version

    @property
    def description(self):
        """description for systemd"""
        return self.__description

    @property
    def app_type(self):
        """type of app"""
        return ""

    @property
    def gateway_access(self):
        return self.__gateway_access

    @property
    def url_prefix(self):
        """url_prefix for running app"""
        return self.__url_prefix

    @property
    def version(self):
        return self.__version

    @property
    def is_asset(self):
        """Accept: "application/octet-stream" needs to be added on headers if it is downloading from assets list"""
        return True

    @abstractmethod
    def select_link(self, row: any, is_browser_downloadable: bool):
        """select_link for selecting builds from GitHub"""
        raise NotImplementedError("select_link needs to be overridden")

    def download(self) -> dict:
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        download_name = download_unzip_service(self.get_download_link(app_setting.token), self.get_download_dir()
                                               , app_setting.token, self.is_asset)
        existing_app_deletion: bool = delete_existing_folder(self.get_downloaded_dir())
        self.after_download(download_name)
        return {'service': self.service(), 'version': self.version, 'existing_app_deletion': existing_app_deletion}

    def after_download(self, download_name: str):
        # they are already wrapped on folder
        download_dir: str = self.get_download_dir()
        extracted_dir = os.path.join(download_dir, download_name)
        os.rename(extracted_dir, self.get_downloaded_dir())

    @abstractmethod
    def install(self) -> bool:
        raise NotImplementedError("install needs to be overridden")

    @abstractmethod
    def uninstall(self) -> bool:
        raise NotImplementedError("uninstall needs to be overridden")

    def restart(self) -> bool:
        logger.info('Restarting Linux Service...')
        if not execute_command('sudo systemctl restart {}'.format(self.service_file_name)):
            return False
        logger.info('Successfully restarted service.')
        return True

    def backup_data(self):
        logger.info('Starting data backup...')
        data_dir = self.get_data_dir()
        if is_dir_exist(data_dir):
            shutil.copytree(data_dir, self.get_backup_dir())
            logger.info('Successfully completed data backup...')
            return True
        return False

    def get_data_dir(self) -> str:
        setting = current_app.config[AppSetting.FLASK_KEY]
        return os.path.join(setting.global_dir, self.data_dir_name)

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


