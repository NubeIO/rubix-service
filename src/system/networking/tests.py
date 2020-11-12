import os
import re

import socket


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


print(valid_ip('10.10.20.'))


