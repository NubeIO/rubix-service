import re
import netifaces


def is_valid_ip(ip):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip):
        return True
    else:
        return False


def is_interface_up(interface):
    try:
        addr = netifaces.ifaddresses(interface)
        return netifaces.AF_INET in addr
    except:
        return False


