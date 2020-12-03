from flask_restful import Resource
import os
from collections import namedtuple

def get_current_memory_usage():
    """ Memory usage in kB """
    with open('/proc/self/status') as f:
        mem_usage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
    return int(mem_usage.strip())


class GetSystemMem(Resource):
    def get(self):
        mem = get_current_memory_usage()
        print()
        return {'mem': mem}






_ntuple_diskusage = namedtuple('usage', 'total used free')


def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0  # 1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


mem = get_current_memory_usage()

print(convert_bytes(mem))
