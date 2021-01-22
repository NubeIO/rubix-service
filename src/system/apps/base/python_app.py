import json
from abc import ABC

import requests
from flask import current_app

from src import AppSetting
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types


class PythonApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.PYTHON_APP.value

    def get_download_link(self, token: str) -> str:
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        release_link = 'https://api.github.com/repos/NubeIO/{}/releases/tags/{}'.format(self.repo_name, self.version)
        resp = requests.get(release_link, headers=headers)
        row = json.loads(resp.content)
        setting = current_app.config[AppSetting.FLASK_KEY]
        for asset in row.get('assets', []):
            if setting.device_type in asset.get('browser_download_url'):
                return asset.get('browser_download_url')
        raise ModuleNotFoundError(
            f'No app for type {setting.device_type} & version {self.version}, check your token & repo')
