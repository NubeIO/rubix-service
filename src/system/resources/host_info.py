import os
import time
from collections import namedtuple
from datetime import datetime, timezone
from flask_restful import Resource

from src.system.resources.utils import format_size, convert_bytes


def host_time():
    dt = datetime.now()
    dt_utc_0 = datetime.now(tz=timezone.utc)
    return {
        'time_utc': dt_utc_0.strftime('%Y-%m-%d %H:%M:%S'),
        'time_local': dt.strftime('%Y-%m-%d %H:%M:%S'),
        'tz_local': time.tzname
    }


def get_current_memory_usage():
    """ Memory usage in kB """
    linux_filepath = "/proc/meminfo"
    meminfo = dict(
        (i.split()[0].rstrip(":"), int(i.split()[1]))
        for i in open(linux_filepath).readlines()
    )

    return {
        'memory_total_gb': format_size(meminfo["MemTotal"], "KB", "GB"),
        'memory_free_gb': format_size(meminfo["MemFree"], "KB", "GB"),
        'memory_available_gb': format_size(meminfo["MemAvailable"], "KB", "GB"),
        'memory_total_mb': format_size(meminfo["MemTotal"], "KB", "MB"),
        'memory_free_mb': format_size(meminfo["MemFree"], "KB", "MB"),
        'memory_available_mb': format_size(meminfo["MemAvailable"], "KB", "MB"),
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


class GetSystemTime(Resource):
    def get(self):
        return host_time()


class GetSystemMem(Resource):
    def get(self):
        return get_current_memory_usage()


class GetSystemDiscUsage(Resource):
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
