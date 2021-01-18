import netifaces
from flask import current_app
from flask_restful import Resource
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger)


def get_all_interfaces():
    ifaces = netifaces.interfaces()
    ifaces_gateway = {}
    gateways = netifaces.gateways()
    interfaces = {}
    gateways = gateways.get(netifaces.AF_INET, [])
    for gateway in gateways:
        ifaces_gateway[gateway[1]] = gateway[0]
    gateways_dict = dict(map(lambda gw: (gw[1], gw[0]), gateways))
    for iface in ifaces:
        if iface not in gateways_dict.keys():
            continue
        try:
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
            macs = netifaces.ifaddresses(iface)[netifaces.AF_LINK]
            addrs = addrs[0]
            macs = macs[0]
            address = addrs.get('addr')
            broadcast = addrs.get('broadcast')
            netmask = addrs.get('netmask')
            mac = macs.get('addr')
            interfaces[iface] = {
                'interface': iface,
                'address': address,
                'broadcast': broadcast,
                'netmask': netmask,
                'gateway': ifaces_gateway.get(iface),
                'mac': mac
            }
        except Exception as e:
            logger.error(str(e))
    return interfaces


class NetworkInfo(Resource):
    def get(self):
        mem = get_all_interfaces()
        return mem
