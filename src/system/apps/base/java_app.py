import os
from abc import ABC

from src.system.apps.base.systemd_app import SystemdApp
from src.system.apps.enums.enums import Types


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
    def name_contains(self) -> str:
        return self.app_setting.name_contains

    def create_service(self):
        lines = []
        with open(os.path.join(self.get_wd(), self.app_setting.systemd_file_dir)) as systemd_file:
            wd: str = self.get_wd()
            for line in systemd_file.readlines():
                if self.app_setting.systemd_static_wd_value in line:
                    line = line.replace(self.app_setting.systemd_static_wd_value, wd)
                lines.append(line)
        return lines
