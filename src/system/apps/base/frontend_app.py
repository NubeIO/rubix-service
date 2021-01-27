from abc import ABC

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types
from src.system.utils.shell import execute_command


class FrontendApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.FRONTEND_APP.value

    @property
    def is_asset(self):
        return False

    def select_link(self, row: any, is_browser_downloadable: bool):
        if is_browser_downloadable:
            return {
                'name': row.get('name'),
                'created_at': row.get('created_at'),
                'browser_download_url': row.get('zipball_url')
            }
        return row.get('zipball_url')

    def install(self) -> bool:
        # TODO: remove user and upgrade parameters in future
        install_cmd: str = "sudo bash script.bash start -service_name={} -u={} -dir={} -data_dir={} -p={}".format(
            self.service_file_name, 'root', self.get_wd(), self.get_data_dir(), self.port)
        return execute_command(install_cmd, self.get_cwd())

    def uninstall(self) -> bool:
        uninstall_cmd: str = "sudo bash script.bash delete"
        return execute_command(uninstall_cmd, self.get_cwd())
