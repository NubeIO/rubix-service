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

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires/systemd')

    def get_wd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires')

    def get_install_cmd(self, user, lib_dir=None) -> str:
        return "sudo bash script.bash start -u={} -dir={}".format(user, self.get_wd())
