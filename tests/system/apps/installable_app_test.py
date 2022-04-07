import subprocess

import gevent


def test2():
    p = subprocess.Popen(["systemctl", "status", "nubeio-rubix-service"], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    print("output", output)


def test():
    for i in range(1000000):
        print(i)
        gevent.spawn(test2)
        # gevent.spawn(read_file, "/data/rubix-registry/device_info.json")
        # read_file("/data/rubix-registry/device_info.json")


if __name__ == "__main__":
    test()
