import os

from src.system.apps.base.frontend_app import FrontendApp


class WiresBuildsApp(FrontendApp):
    def __init__(self):
        super(WiresBuildsApp, self).__init__(
            display_name='Rubix Wires',
            repo_name='wires-builds',
            service_file_name='nubeio-rubix-wires.service',
            data_dir_name='rubix-wires',
            port=1313,
            min_support_version='v1.8.7',
            description='Wires for for IoT',
            need_wires_plat=True,
        )

    @classmethod
    def service(cls) -> str:
        return 'WIRES'

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires/systemd')

    def get_wd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires')
