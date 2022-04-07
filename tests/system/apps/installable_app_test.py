import gevent

from src.system.utils.file import read_file


def test():
    for i in range(1000000):
        print(i)
        gevent.spawn(read_file, "/data/rubix-registry/device_info.json")
        # read_file("/data/rubix-registry/device_info.json")


if __name__ == "__main__":
    test()
