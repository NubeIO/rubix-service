from src.system.apps.base.installable_app import InstallableApp


class PointServerApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'POINT_SERVER'

    def name(self) -> str:
        return 'rubix-point-server'

    def service_file_name(self) -> str:
        return 'nubeio-point-server.service'

    def data_dir_name(self) -> str:
        return 'point-server'

    def port(self) -> int:
        """port for running app"""
        return 1515
