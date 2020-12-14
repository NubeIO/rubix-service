import os

from src.system.apps.base.installable_app import InstallableApp


class RubixPlatBuildApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'RUBIX_PLAT'

    def name(self) -> str:
        return 'rubix-plat-build'

    def data_dir_name(self) -> str:
        return 'rubix-plat-build'

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-plat')

    def get_wd(self) -> str:
        return self.get_cwd()

    def get_install_cmd(self, user, lib_dir=None) -> str:
        return "sudo bash script.bash start -u={} -dir={}".format(user, self.get_wd())
