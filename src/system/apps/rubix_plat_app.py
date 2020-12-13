from src.system.apps.base.installable_app import InstallableApp


class RubixPlatApp(InstallableApp):
    @classmethod
    def id(cls) -> str:
        return 'RUBIX_PLAT'

    def name(self) -> str:
        return 'rubix-plat-build'

    def data_dir_name(self) -> str:
        return 'rubix-plat'
