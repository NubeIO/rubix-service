import os

from src.system.apps.base.installable_app import InstallableApp


class RubixPlatBuildApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'RUBIX_PLAT'

    def name(self) -> str:
        return 'rubix-plat-build'

    def service_file_name(self) -> str:
        return 'rubix'

    def data_dir_name(self) -> str:
        return 'rubix-plat-build'

    def port(self) -> int:
        return 1414

    def min_support_version(self) -> str:
        return 'v1.1.6'

    def gateway_access(self) -> bool:
        return False

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-plat')

    def get_wd(self) -> str:
        return self.get_cwd()
