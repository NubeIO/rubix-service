import time
from datetime import datetime

from rubix_http.resource import RubixResource

from src.discover.remote_device_registry import RemoteDeviceRegistry

start_time = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - start_time


class RemoteDevice(RubixResource):

    @classmethod
    def get(cls):
        return RemoteDeviceRegistry().devices
