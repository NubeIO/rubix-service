import os
from abc import abstractmethod, ABC

from flask import current_app
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import inheritors

logger = LocalProxy(lambda: current_app.logger)


class InstallableApp(ABC):

    def __init__(self):
        self.version = ""

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

    @abstractmethod
    def name(self) -> str:
        """name for installation folder creation and github repo name validation"""
        raise NotImplementedError("name needs to be overridden")

    @abstractmethod
    def service_file_name(self) -> str:
        """service_file_name for systemd name"""
        raise NotImplementedError("service_file_name needs to be overridden")

    def description(self) -> str:
        """description for systemd"""
        return ""

    @abstractmethod
    def data_dir_name(self) -> str:
        """data_dir_name for making/denoting a valid data dir"""
        raise NotImplementedError("services needs to be overridden")

    @abstractmethod
    def port(self) -> int:
        """port for running app"""
        raise NotImplementedError("port needs to be overridden")

    def url_prefix(self) -> str:
        return ""

    def gateway_access(self) -> bool:
        return True

    @abstractmethod
    def min_support_version(self) -> str:
        raise NotImplementedError("min_support_version needs to be overridden")

    def get_data_dir(self) -> str:
        setting = current_app.config[AppSetting.KEY]
        return os.path.join(setting.global_dir, self.data_dir_name())

    def get_releases_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/releases'.format(self.name())

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
        return os.path.join(setting.artifact_dir, 'download', self.name())

    def get_installation_dir(self) -> str:
        setting = current_app.config[AppSetting.KEY]
        return os.path.join(setting.artifact_dir, 'install', self.name())

    def get_downloaded_dir(self):
        return os.path.join(self.get_download_dir(), self.version)

    def get_installed_dir(self):
        return os.path.join(self.get_installation_dir(), self.version)

    def set_version(self, version):
        self.version = version
