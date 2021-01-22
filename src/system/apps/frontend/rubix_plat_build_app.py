import os

from src.system.apps.base.frontend_app import FrontendApp


class RubixPlatBuildApp(FrontendApp):
    def __init__(self):
        super(RubixPlatBuildApp, self).__init__(
            display_name='Rubix Plat',
            repo_name='rubix-plat-build',
            service_file_name='nubeio-wires-plat.service',
            data_dir_name='rubix-plat-build',
            port=1414,
            min_support_version='v1.1.6',
            description='Rubix Platform',
        )

    @classmethod
    def service(cls) -> str:
        return 'RUBIX_PLAT'

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-plat')

    def get_wd(self) -> str:
        return self.get_cwd()
