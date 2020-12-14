import logging
import os
from abc import abstractmethod

from src.system.utils.file import get_extracted_dir

logger = logging.getLogger(__name__)


class InstallableApp(object):
    __app_parent_dir = '/nube-apps'
    __data_parent_dir = '/data'

    @classmethod
    def get_app(cls, service):
        for subclass in InstallableApp.__subclasses__():
            if subclass.id() == service:
                return subclass()
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

    def get_download_link(self, version) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/zipball/{}'.format(self.name(), version)

    def get_cwd(self) -> str:
        """current working dir for script.bash execution"""
        cwd = get_extracted_dir(self.installation_dir())
        if not cwd:
            raise Exception("Check {}, we don't have any files inside this dir".format(self.installation_dir()))
        return cwd

    def get_wd(self) -> str:
        """working dir for systemd working directory set"""
        return self.get_cwd()

    def get_install_cmd(self, user, lib_dir=None) -> str:
        return "sudo bash script.bash start -u={} -dir={} -lib_dir={}".format(user, self.get_wd(), lib_dir)

    def get_delete_command(self) -> str:
        return "sudo bash script.bash delete"

    def installation_dir(self) -> str:
        return os.path.join(InstallableApp.__app_parent_dir, self.name())
