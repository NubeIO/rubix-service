from abc import ABC

from flask import current_app

from src import AppSetting
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types


class PythonApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.PYTHON_APP.value

    def select_asset(self, row: any):
        setting = current_app.config[AppSetting.FLASK_KEY]
        for asset in row.get('assets', []):
            if setting.device_type in asset.get('name'):
                return asset.get('url')
