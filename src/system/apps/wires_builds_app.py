import os

from src.system.apps.base.installable_app import InstallableApp


class WiresBuildsApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'WIRES'

    def name(self) -> str:
        return 'wires-builds'

    def service_file_name(self) -> str:
        return 'nubeio-rubix-wires.service'

    def data_dir_name(self) -> str:
        return 'rubix-wires'

    def port(self) -> int:
        """port for running app"""
        return 1313

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires/systemd')

    def get_wd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires')
