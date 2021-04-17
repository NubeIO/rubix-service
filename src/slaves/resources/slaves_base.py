import json
import os

from flask import current_app
from rubix_http.resource import RubixResource

from src import AppSetting
from src.system.utils.file import read_file


class SlavesBase(RubixResource):

    @classmethod
    def get_slaves(cls) -> tuple:
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        data_dir: str = app_setting.data_dir
        slaves_file = os.path.join(data_dir, AppSetting.default_slaves_file)
        slaves: list = json.loads(read_file(slaves_file) or "[]")
        return slaves, slaves_file
