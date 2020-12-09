from src.system.apps.base.installable_app import InstallableApp


class PointServerApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'BAC_REST'

    def name(self) -> str:
        return 'point-server'

    def service_file_name(self) -> str:
        return 'nubeio-point-server.service'
