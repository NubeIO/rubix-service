import os
from abc import abstractmethod, ABC

from flask import current_app
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import inheritors
from src.model import BaseModel

logger = LocalProxy(lambda: current_app.logger)


class InstallableApp(BaseModel, ABC):

    def __init__(self, repo_name, service_file_name, data_dir_name, port, min_support_version, description='',
                 gateway_access=False, url_prefix='', version=''):

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
            if subclass.id() == service:
                instance = subclass()
                instance.version = version
                return instance
        raise ModuleNotFoundError("service {} does not exist in our system".format(service))

    @classmethod
    @abstractmethod
    def id(cls) -> str:
        """id for mapping frontend request with the App"""
        raise NotImplementedError("id needs to be overridden")

    @property
    def repo_name(self):
        """name for installation folder creation and github repo name validation"""
        return self.__repo_name

    @property
    def service_file_name(self):
        """service_file_name for systemd name"""
        return self.__service_file_name

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

    def get_data_dir(self) -> str:
        setting = current_app.config[AppSetting.KEY]
        return os.path.join(setting.global_dir, self.data_dir_name)

    def get_releases_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/releases'.format(self.repo_name)

    def get_download_link(self) -> str:
        raise NotImplementedError("get_download_link logic needs to be overridden")

    def get_cwd(self) -> str:
        """current working dir for script.bash execution"""
        return self.get_installed_dir()

    def get_wd(self) -> str:
        """working dir for systemd working directory set"""
        return self.get_installed_dir()

    def get_download_dir(self) -> str:
        setting = current_app.config[AppSetting.KEY]
        return os.path.join(setting.artifact_dir, 'download', self.repo_name)

    def get_installation_dir(self) -> str:
        setting = current_app.config[AppSetting.KEY]
        return os.path.join(setting.artifact_dir, 'install', self.repo_name)

    def get_downloaded_dir(self):
        return os.path.join(self.get_download_dir(), self.__version)

    def get_installed_dir(self):
        return os.path.join(self.get_installation_dir(), self.__version)
