import json
from abc import ABC

import requests
from flask import current_app

from src import AppSetting
from src.system.apps.base.installable_app import InstallableApp


class PythonApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return "PythonApp"

    def get_download_link(self) -> str:
        resp = requests.get(self.get_releases_link())
        data = json.loads(resp.content)
        for row in data:
            for asset in row.get('assets', []):
                setting = current_app.config[AppSetting.KEY]
                if setting.device_type in asset.get('browser_download_url'):
                    return asset.get('browser_download_url')
        return ""
