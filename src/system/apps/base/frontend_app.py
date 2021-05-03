import os
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

    def get_cwd(self) -> str:
        if self.app_setting.current_working_dir_name:
            return os.path.join(super().get_cwd(), self.app_setting.current_working_dir_name)
        return super().get_cwd()

    def get_wd(self) -> str:
        if self.app_setting.working_dir_name:
            return os.path.join(super().get_cwd(), self.app_setting.working_dir_name)
        return self.get_cwd()

    def select_link(self, row: any, is_browser_downloadable: bool):
        if is_browser_downloadable:
            return {
                'name': row.get('name'),
                'created_at': row.get('created_at'),
                'browser_download_url': row.get('zipball_url')
            }
        return row.get('zipball_url')

    def install(self) -> bool:
        install_cmd: str = f"sudo bash script.bash install -s={self.service_file_name} -u=root " \
                           f"--working-dir={self.get_wd()} -g={self.get_global_dir()} -d=data -c=config -p {self.port}"
        return execute_command(install_cmd, self.get_cwd())

    def uninstall(self) -> bool:
        uninstall_cmd: str = "sudo bash script.bash delete"
        return execute_command(uninstall_cmd, self.get_cwd())
