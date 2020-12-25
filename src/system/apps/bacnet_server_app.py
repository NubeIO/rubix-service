from src.system.apps.base.installable_app import InstallableApp


class BACnetServerApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'BACNET_SERVER'

    def name(self) -> str:
        return 'rubix-bacnet-server'

    def service_file_name(self) -> str:
        return 'nubeio-bacnet-server.service'

    def data_dir_name(self) -> str:
        return 'bacnet-server'

    def port(self) -> int:
        """port for running app"""
        return 1717

    def url_prefix(self) -> str:
        return '/bacnet'
