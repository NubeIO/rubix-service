from abc import ABC

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types


class FrontendApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.FRONTEND_APP.value

    def get_download_link(self) -> str:
        return 'https://api.github.com/repos/NubeIO/{}/zipball/{}'.format(self.repo_name, self.version)

    def get_install_cmd(self) -> str:
        # TODO: remove user and upgrade parameters in future
        return "sudo bash script.bash start -service_name={} -u={} -dir={} -data_dir={} -p={}".format(
            self.service_file_name, 'root', self.get_wd(), self.get_data_dir(), self.port)

    @staticmethod
    def get_delete_command() -> str:
        return "sudo bash script.bash delete"
