from abc import ABC, abstractmethod

from src.system.apps.base.systemd_app import SystemdApp
from src.system.apps.enums.types import Types


class JavaApp(SystemdApp, ABC):
    @property
    def app_type(self):
        return Types.JAVA_APP.value

    def select_link(self, row: any, is_browser_downloadable: bool):
        for asset in row.get('assets', []):
            if self.name_contains in asset.get('name'):
                if is_browser_downloadable:
                    return {
                        'name': row.get('name'),
                        'created_at': row.get('created_at'),
                        'browser_download_url': asset.get('browser_download_url')
                    }
                return asset.get('url')

    @property
    @abstractmethod
    def name_contains(self) -> str:
        raise NotImplementedError("name_contains needs to be overridden")
