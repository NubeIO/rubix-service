import time
from datetime import datetime

import toml
from flask import current_app
from flask_restful import Resource

from src import AppSetting
from src.pyinstaller import resource_path

startTime = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - startTime


class Ping(Resource):
    def get(self):
        details = toml.load(resource_path("pyproject.toml"))
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = "{:.2f}".format(up_min)
        up_hour = up_time / 3600
        up_hour = "{:.2f}".format(up_hour)
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        deployment_mode = 'production' if setting.prod else 'development'
        return {
            'version': details.get('tool', {}).get('poetry', {}).get('version'),
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
        }
