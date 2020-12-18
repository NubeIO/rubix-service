import enum
import socket


class PointType(enum.Enum):
    DHCP = 0
    STATIC = 1


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False
