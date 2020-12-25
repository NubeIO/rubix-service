import os
from abc import abstractmethod

from flask import current_app
from werkzeug.local import LocalProxy

# noinspection PyTypeChecker
logger = LocalProxy(lambda: current_app.logger)


class InstallableApp:

    def __init__(self):
        self.version = ""

    @classmethod
    def get_app(cls, service, version):
        for subclass in InstallableApp.__subclasses__():
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
        setting = current_app.config['SETTING']
        return os.path.join(setting.global_dir, self.data_dir_name())

    def get_releases_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/releases'.format(self.name(), self.version)

    def get_download_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/zipball/{}'.format(self.name(), self.version)

    def get_downloaded_dir(self):
        return os.path.join(self.get_installation_dir(), self.version)

    def get_cwd(self) -> str:
        """current working dir for script.bash execution"""
        return self.get_downloaded_dir()

    def get_wd(self) -> str:
        """working dir for systemd working directory set"""
        return self.get_downloaded_dir()

    def get_install_cmd(self, lib_dir=None) -> str:
        # TODO: remove user and upgrade parameters in future
        return "sudo bash script.bash start -service_name={} -u={} -dir={} -lib_dir={} -data_dir={} -p={}" \
            .format(self.service_file_name(), 'root', self.get_wd(), lib_dir, self.get_data_dir(), self.port())

    def get_delete_command(self) -> str:
        return "sudo bash script.bash delete"

    def get_installation_dir(self) -> str:
        setting = current_app.config['SETTING']
        return os.path.join(setting.artifact_dir, self.name())

    def set_version(self, version):
        self.version = version
