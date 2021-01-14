from flask_restful import Resource
import os
from collections import namedtuple
from datetime import datetime
import time

from src.users.authorize_users import authorize


def host_time():
    return {
        'time_utc': str(datetime.now()),
        'time_local': str(datetime.utcnow()),
        'tz_local': time.tzname

    }


def get_current_memory_usage():
    """ Memory usage in kB """
    linux_filepath = "/proc/meminfo"
    meminfo = dict(
        (i.split()[0].rstrip(":"), int(i.split()[1]))
        for i in open(linux_filepath).readlines()
    )
    memory_total_gb = meminfo["memory_total_gb"] = meminfo["MemTotal"] / (2 ** 20)
    memory_free_gb = meminfo["memory_free_gb"] = meminfo["MemFree"] / (2 ** 20)
    memory_available_gb = meminfo["memory_available_gb"] = meminfo["MemAvailable"] / (2 ** 20)
    memory_total_mb = memory_total_gb / 1000
    memory_free_mb = memory_free_gb / 1000
    memory_available_mb = memory_available_gb / 1000
    return {
        'memory_total_gb': memory_total_gb,
        'memory_free_gb': memory_free_gb,
        'memory_available_gb': memory_available_gb,
        'memory_total_mb': memory_total_mb,
        'memory_free_mb': memory_free_mb,
        'memory_available_mb': memory_available_mb,
    }


def disk_usage(path):
    """Return disk usage statistics about the given path.
    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    _tuple = namedtuple('usage', 'total used free')
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _tuple(free, total, used)


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0  # 1024 bad the size
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


class GetSystemTime(Resource):
    @authorize
    def get(self):
        return host_time()


class GetSystemMem(Resource):
    @authorize
    def get(self):
        return get_current_memory_usage()


class GetSystemDiscUsage(Resource):
    @authorize
    def get(self):
        path = '/'
        du = disk_usage(path)
        free = convert_bytes(du[0])
        total = convert_bytes(du[1])
        used = convert_bytes(du[2])
        return {
            'free': free,
            'total': total,
            'used': used
        }
