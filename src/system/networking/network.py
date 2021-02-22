import netifaces
from flask import current_app
from rubix_http.exceptions.exception import BadDataException
from rubix_http.resource import RubixResource
from werkzeug.local import LocalProxy
from flask_restful import reqparse

from src.system.networking.ip import dhcpcdManager
from src.system.networking.ping import network_ping_range, port_check_udp, port_check_tcp
from src.system.networking.utils import is_valid_ip, is_interface_up

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
    return interfaces


class NetworkInfo(RubixResource):
    def get(self):
        mem = get_all_interfaces()
        return mem


class NetworkSetStaticIP(RubixResource):
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
        parser.add_argument('network_reset',
                            type=bool,
                            help='Will reset networking`',
                            required=True)
        args = parser.parse_args()
        interface = args['interface']
        if not is_interface_up(interface):
            raise BadDataException("interface is not valid")
        ip_address = args['ip_address']
        if not is_valid_ip(ip_address):
            raise BadDataException("ip address is not valid")
        routers = args['routers']
        if not is_valid_ip(routers):
            raise BadDataException("routers address is not valid")
        if not is_valid_ip(routers):
            raise BadDataException("routers address is not valid")
        domain_name_server = args['domain_name_server']
        if not is_valid_ip(domain_name_server):
            raise BadDataException("domain_name_server address is not valid")
        netmask = args['netmask']
        if not is_valid_ip(netmask):
            raise BadDataException("netmask address is not valid")

        reset = args['network_reset']
        ip = dhcpcdManager()
        ip.set_static_info(interface, ip_address, routers, domain_name_server, netmask)
        if reset:
            ip.restart_interface(interface)
        return True


class NetworkSetDHCP(RubixResource):
    """
    ip.set_static_info('eth0', true)  # add a static ip
    """

    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('interface',
                            type=str,
                            help='example `192.168.15`',
                            required=True)
        parser.add_argument('network_reset',
                            type=bool,
                            help='Will reset networking`',
                            required=True)
        args = parser.parse_args()
        interface = args['interface']
        reset = args['network_reset']
        if not is_interface_up(interface):
            raise BadDataException("interface is not valid")
        ip = dhcpcdManager()
        ip.remove_static_info(interface)
        if reset:
            ip.restart_interface(interface)
        return True


class NetworkPingRange(RubixResource):
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('address',
                            type=str,
                            help='example `start a 1 192.168.15.x(1)`',
                            required=True)
        parser.add_argument('start_address',
                            type=int,
                            help='example `start a 1 192.168.15.x(1)`',
                            required=True)
        parser.add_argument('end_address',
                            type=int,
                            help='example `finish a 10 192.168.15.x(10)`',
                            required=True)
        parser.add_argument('timeout_seconds',
                            type=int,
                            help='time out to wait for replay',
                            required=True)
        args = parser.parse_args()
        address = args['address']
        start = args['start_address']
        finish = args['end_address']
        timeout_seconds = args['timeout_seconds']
        return network_ping_range(address, start, finish, timeout_seconds)


class NetworkCheckPort(RubixResource):
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('host',
                            type=str,
                            help='example `start a 1 192.168.15.1`',
                            required=True)
        parser.add_argument('port',
                            type=int,
                            help='example `502`',
                            required=True)
        parser.add_argument('type_udp',
                            type=bool,
                            help='set to true for port type UDP`',
                            required=True)
        args = parser.parse_args()
        host = args['host']
        port = args['port']
        type_udp = args['type_udp']
        if type_udp:
            return port_check_udp(host, port)
        else:
            return port_check_tcp(host, port)
