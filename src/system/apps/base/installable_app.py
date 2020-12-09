import os
from abc import abstractmethod

from src.system.utils.file import get_extracted_dir


class InstallableApp(object):
    __app_parent_dir = '/nube-apps'

    @classmethod
    def get_app(cls, service):
        for subclass in InstallableApp.__subclasses__():
            if subclass.id() == service:
                return subclass()
        raise Exception("service {} does not exist in our system".format(service))

    @classmethod
    @abstractmethod
    def id(cls) -> str:
        raise Exception("InstallableApp id needs to be overridden")

    @abstractmethod
    def name(self) -> str:
        raise Exception("InstallableApp name needs to be overridden")

    @abstractmethod
    def service_file_name(self) -> str:
        raise Exception("InstallableApp services needs to be overridden")

    def get_domain(self) -> tuple:
        return 'api.github.com', 'NubeIO', self.name()

    def get_cwd(self) -> str:
        """current working dir for script.bash execution"""
        cwd = get_extracted_dir(self.installation_dir())
        if not cwd:
            raise Exception("Check {}, we don't have any files inside this dir".format(self.installation_dir()))
        return cwd

    def get_wd(self) -> str:
        """working dir for systemd working directory set"""
        return self.get_cwd()

    def get_delete_data_command(self) -> str:
        return "sudo bash script.bash delete_data"

    def get_delete_command(self) -> str:
        return "sudo bash script.bash delete"

    def get_install_cmd(self, user, lib_dir=None) -> str:
        return "sudo bash script.bash start -u={} -dir={} -lib_dir={}".format(user, self.get_wd(), lib_dir)

    def installation_dir(self) -> str:
        return os.path.join(InstallableApp.__app_parent_dir, self.name())

    def validate_domain(self, url) -> bool:
        u = url.split("/")
        domain = (u[2], u[4], u[5])
        app_domain = self.get_domain()
        print("URL check:", domain, app_domain)
        return app_domain == domain
