from datetime import datetime

import time
from flask import current_app
from flask_restful import Resource
from werkzeug.local import LocalProxy

# noinspection PyTypeChecker
logger = LocalProxy(lambda: current_app.logger)

startTime = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - startTime


class Ping(Resource):
    def get(self):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = "{:.2f}".format(up_min)
        up_hour = up_time / 3600
        up_hour = "{:.2f}".format(up_hour)
        logger.info('ping here')
        return {
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour
        }
