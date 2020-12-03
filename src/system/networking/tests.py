import os
import re

import socket


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


print(valid_ip('192.168.0.237'))


import netifaces

iface = netifaces.interfaces()
print(iface)
wan = netifaces.ifaddresses('enp0s31f6')
print(wan[netifaces.AF_INET])
print(wan[netifaces.AF_LINK])
print(netifaces.gateways())


from socket import gethostname

def whereami():
    res = 'Hostname: ' + gethostname() + '\n'
    for interface in netifaces.interfaces():
        for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
            res += 'IP: ' + link['addr'] + '\n'
    return res


print(whereami())