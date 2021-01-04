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
        resp = requests.get(self.get_selected_releases_link())
        row = json.loads(resp.content)
        setting = current_app.config[AppSetting.KEY]
        for asset in row.get('assets', []):
            if setting.device_type in asset.get('browser_download_url'):
                return asset.get('browser_download_url')
        raise ModuleNotFoundError('No app for type {} & version {}'.format(setting.device_type, self.__version))
