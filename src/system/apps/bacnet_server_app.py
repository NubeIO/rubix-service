from src.system.apps.base.installable_app import InstallableApp


class BACnetServerApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'BACNET_SERVER'

    def name(self) -> str:
        return 'rubix-bacnet-server'

    def data_dir_name(self) -> str:
        return 'bacnet-server'
