import json
from abc import ABC

import requests
from flask import current_app

from src import AppSetting
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.constants.types import PYTHON_APP


class PythonApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return PYTHON_APP

    def get_download_link(self) -> str:
        release_link = 'https://api.github.com/repos/NubeIO/{}/releases/tags/{}'.format(self.repo_name, self.version())
        resp = requests.get(release_link)
        row = json.loads(resp.content)
        setting = current_app.config[AppSetting.FLASK_KEY]
        for asset in row.get('assets', []):
            if setting.device_type in asset.get('browser_download_url'):
                return asset.get('browser_download_url')
        raise ModuleNotFoundError('No app for type {} & version {}'.format(setting.device_type, self.version()))
