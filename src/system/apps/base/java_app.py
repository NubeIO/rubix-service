from abc import ABC, abstractmethod

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types


class JavaApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.JAVA_APP.value

    def select_asset(self, row: any):
        for asset in row.get('assets', []):
            if self.name_contains in asset.get('name'):
                return asset.get('url')

    @property
    @abstractmethod
    def name_contains(self) -> str:
        raise NotImplementedError("name_contains needs to be overridden")

    def after_download(self, download_name: str):
        pass

    def install(self):
        pass

    def uninstall(self):
        pass

    def restart(self):
        pass
