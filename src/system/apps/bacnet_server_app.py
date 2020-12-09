from src.system.apps.base.installable_app import InstallableApp


class BACnetServerApp(InstallableApp):
    def id(self) -> str:
        return 'BAC_SERVER'

    def name(self) -> str:
        return 'bacnet-server'

    def service_file_name(self) -> str:
        return 'nubeio-bacnet-server.service'

