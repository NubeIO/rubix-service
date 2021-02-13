import netifaces
from flask import current_app
from werkzeug.local import LocalProxy
from flask_restful import Resource, reqparse, abort

from src.system.networking.ip import dhcpcdManager
from src.system.networking.utils import is_valid_ip

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


class NetworkSetStaticIP(Resource):
    """
    ip.set_static_info(iface, "192.168.15.7", "192.168.15.1", "8.8.8.8", "255.255.255.0")  # add a static ip
    """
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('interface',
                            type=str,
                            help='example `eth0`',
                            required=True)
        parser.add_argument('ip_address',
                            type=str,
                            help='example `192.168.15.1`',
                            required=True)
        parser.add_argument('routers',
                            type=str,
                            help='example `192.168.15.1`',
                            required=True)
        parser.add_argument('domain_name_server',
                            type=str,
                            help='example `8.8.8.8`',
                            required=True)
        parser.add_argument('netmask',
                            type=str,
                            help='example `255.255.255.0`',
                            required=True)
        args = parser.parse_args()
        interface = args['interface']
        ip_address = args['ip_address']
        if not is_valid_ip(ip_address):
            abort(500, message=str("ip address is not valid"))
        routers = args['routers']
        if not is_valid_ip(routers):
            abort(500, message=str("routers address is not valid"))
        if not is_valid_ip(routers):
            abort(500, message=str("routers address is not valid"))
        domain_name_server = args['domain_name_server']
        if not is_valid_ip(domain_name_server):
            abort(500, message=str("domain_name_server address is not valid"))
        netmask = args['netmask']
        if not is_valid_ip(netmask):
            abort(500, message=str("netmask address is not valid"))
        try:
            ip = dhcpcdManager()
            ip.set_static_info(interface, ip_address, routers, domain_name_server, netmask)  # add a static ip
            return {}
        except Exception as e:
            abort(501, message=str(e))
