import enum
import os
from flask_restful import Resource, reqparse, abort
from src.system.utils.shell_commands import execute_command, systemctl_status_check



class ServiceAction(enum.Enum):
    true = 0
    false = 1

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
            call = get_interface()
            if call is not None:
                set_dhcp_command(call)
                return {'msg': call, 'status': True, 'fail': False}
            else:
                return {'msg': call, 'status': False, 'fail': True}
        else:
            msg = "update to interface to DHCP fail"
            return {'msg': msg, 'status': False, 'fail': False}, 404
