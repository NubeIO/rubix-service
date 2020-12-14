import logging
import os
from abc import abstractmethod

logger = logging.getLogger(__name__)


class InstallableApp(object):
    __app_parent_dir = '/nube-apps'
    __data_parent_dir = '/data'

    def __init__(self):
        self.version = ""

    @classmethod
    def get_app(cls, service, version):
        for subclass in InstallableApp.__subclasses__():
            if subclass.id() == service:
                instance = subclass()
                instance.version = version
                return instance
        raise Exception("service {} does not exist in our system".format(service))

    @classmethod
    @abstractmethod
    def id(cls) -> str:
        """id for mapping frontend request with the App"""
        raise Exception("InstallableApp id needs to be overridden")

    @abstractmethod
    def name(self) -> str:
        """name for installation folder creation and github repo name validation"""
        raise Exception("InstallableApp name needs to be overridden")

    @abstractmethod
    def data_dir_name(self) -> str:
        """data_dir_name for making/denoting a valid data dir"""
        raise Exception("InstallableApp services needs to be overridden")

    def get_data_dir(self) -> str:
        return os.path.join(InstallableApp.__data_parent_dir, self.data_dir_name())

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

    def get_install_cmd(self, user, lib_dir=None) -> str:
        return "sudo bash script.bash start -u={} -dir={} -lib_dir={}".format(user, self.get_wd(), lib_dir)

    def get_delete_command(self) -> str:
        return "sudo bash script.bash delete"

    def get_installation_dir(self) -> str:
        return os.path.join(InstallableApp.__app_parent_dir, self.name())

    def set_version(self, version):
        self.version = version
