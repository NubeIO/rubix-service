import enum

from numpy import long


class PointType(enum.Enum):
    DHCP = 0
    STATIC = 1


import socket


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False

