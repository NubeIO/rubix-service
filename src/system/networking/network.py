import netifaces
from flask import current_app
from werkzeug.local import LocalProxy
from flask_restful import Resource, reqparse, abort

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
        parser.add_argument('network_reset',
                            type=bool,
                            help='Will reset networking`',
                            required=True)
        args = parser.parse_args()
        interface = args['interface']
        if not is_interface_up(interface):
            abort(500, message=str("interface is not valid"))
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

        reset = args['network_reset']
        try:
            ip = dhcpcdManager()
            ip.set_static_info(interface, ip_address, routers, domain_name_server, netmask)
            if reset:
                try:
                    ip.restart_interface(interface)
                except Exception as e:
                    abort(501, message=str(e))
            return True
        except Exception as e:
            abort(501, message=str(e))


class NetworkSetDHCP(Resource):
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
            abort(500, message=str("interface is not valid"))
        try:
            ip = dhcpcdManager()
            ip.remove_static_info(interface)
            if reset:
                try:
                    ip.restart_interface(interface)
                except Exception as e:
                    abort(501, message=str(e))
            return True
        except Exception as e:
            abort(501, message=str(e))


class NetworkPingRange(Resource):
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
        try:
            return network_ping_range(address, start, finish, timeout_seconds)
        except Exception as e:
            abort(501, message=str(e))


class NetworkCheckPort(Resource):
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
        try:
            if type_udp:
                return port_check_udp(host, port)
            else:
                return port_check_tcp(host, port)
        except Exception as e:
            abort(501, message=str(e))
