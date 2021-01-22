import json
import os
from abc import abstractmethod, ABC

import requests
from flask import current_app

from src import AppSetting
from src.inheritors import inheritors
from src.model import BaseModel


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
    def select_asset(self, row: any):
        """select_asset for selecting builds from GitHub"""
        raise NotImplementedError("select_asset needs to be overridden")

    def get_data_dir(self) -> str:
        setting = current_app.config[AppSetting.FLASK_KEY]
        return os.path.join(setting.global_dir, self.data_dir_name)

    def get_releases_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/releases'.format(self.repo_name)

    def get_download_link(self, token: str) -> str:
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        release_link: str = f'https://api.github.com/repos/NubeIO/{self.repo_name}/releases/tags/{self.version}'
        resp = requests.get(release_link, headers=headers)
        row: str = json.loads(resp.content)
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        download_link: str = self.select_asset(row)
        if not download_link:
            raise ModuleNotFoundError(
                f'No app for type {setting.device_type} & version {self.version}, check your token & repo')
        return download_link

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

    def set_version(self, _version):
        self.__version = _version
