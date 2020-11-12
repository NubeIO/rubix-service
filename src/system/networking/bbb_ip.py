import enum
import os
import socket

from flask_restful import Resource, reqparse, abort
from src.system.utils.shell_commands import execute_command, systemctl_status_check


class ServiceAction(enum.Enum):
    true = 0
    false = 1


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def _validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart`')


def get_interface():
    try:
        res = os.popen('connmanctl services').read()
        res = res.replace('*AO Wired', '')  # remove word
        res = " ".join(res.split())  # white space
    except:
        return None
    return res


def set_dhcp_command(iface):
    command = "sudo connmanctl config {} --ipv4 dhcp".format(iface)
    return command


def set_staic_command(iface, ip, sub, gate):
    command = "sudo connmanctl config {} --ipv4 manual {} {} {} --nameservers 8.8.8.8 8.8.4.4".format(iface, ip,
                                                                                                      sub, gate)
    return command



class BBB_DHCP(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=bool, help='action should be `true or false`', required=True)
        args = parser.parse_args()
        action = args['action']
        if action:
            # interface = get_interface()
            interface = "ethernet_4c3fd3322f59_cable"
            if interface is not None:
                cmd = set_dhcp_command(interface)
                # TODO add setip
                return {'msg': cmd, 'interface': interface, 'status': True, 'fail': False}
            else:
                return {'msg': None, 'interface': None, 'status': False, 'fail': True}
        else:
            msg = "update to interface to DHCP fail"
            return {'msg': msg, 'status': False, 'fail': False}, 404


class BBB_STAIC(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, help='should be an IP address', required=True)
        parser.add_argument('sub', type=str, help='should be an sub address`', required=True)
        parser.add_argument('gate', type=str, help='should be an gateway address', required=True)
        args = parser.parse_args()
        ip = args['ip']
        sub = args['sub']
        gate = args['gate']
        check = valid_ip(ip)
        if not check:
            return {'msg': 'ip is not vaild', 'status': False, 'fail': False}, 404
        check = valid_ip(sub)
        if not check:
            return {'msg': 'subnet is not vaild', 'status': False, 'fail': False}, 404
        check = valid_ip(gate)
        if not check:
            return {'msg': 'gateway is not vaild', 'status': False, 'fail': False}, 404
        # interface = get_interface()
        interface = "ethernet_4c3fd3322f59_cable"
        if interface is not None:
            cmd = set_staic_command(interface, ip, sub, gate)
            # TODO add setip
            return {'msg': cmd, 'interface': interface, 'status': True, 'fail': False}
        else:
            return {'msg': None, 'interface': None, 'status': False, 'fail': True}
