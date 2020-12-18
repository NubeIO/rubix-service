import netifaces
from flask_restful import Resource


def get_all_interfaces():
    ifaces = netifaces.interfaces()
    ifaces_gateway = {}
    gateways = netifaces.gateways()
    interfaces = {}
    default_gateway = gateways.get('default', {}).get(netifaces.AF_INET)
    gateways = gateways.get(netifaces.AF_INET, []) + \
               [default_gateway] if default_gateway else []
    for gateway in gateways:
        ifaces_gateway[gateway[1]] = gateway[0]
    for iface in ifaces:
        if iface == 'lo':
            continue
        addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
        macs = netifaces.ifaddresses(iface)[netifaces.AF_LINK]
        if not addrs:
            continue
        addrs = addrs[0]
        macs = macs[0]
        address = addrs.get('addr')
        if not address:
            continue
        broadcast = addrs.get('broadcast')
        if not broadcast:
            continue
        netmask = addrs.get('netmask')
        if not netmask:
            continue
        mac = macs.get('addr')
        if not netmask:
            continue
        interfaces[iface] = {
            'interface': iface,
            'address': address,
            'broadcast': broadcast,
            'netmask': netmask,
            'gateway': ifaces_gateway.get(iface),
            'mac': mac
        }
    return interfaces


class NetworkInfo(Resource):
    def get(self):
        mem = get_all_interfaces()
        return mem

# print(get_all_interfaces())
