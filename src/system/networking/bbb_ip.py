import enum
from flask_restful import Resource, reqparse, abort
from src.system.utils.shell_commands import execute_command, systemctl_status_check

interface = 'eth0'
dhcp_static = True
ip = "body.eth1Ip;"
sub = "body.eth1Ip;"
gate = "body.eth1Ip;"
name_server = "body.eth1Ip;"



# setIP = `sudo connmanctl config ${iface} --ipv4 manual ${ipAddress} ${subnetMask} ${gateway} --nameservers 8.8.8.8 8.8.4.4`;
# setIpDHCP = `sudo connmanctl config ${iface} --ipv4 dhcp`;

class ServiceAction(enum.Enum):
    START = 1
    STOP = 2
    RESTART = 3


class Services(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    PLAT = 'nubeio-wires-plat.service'
    MOSQUITTO = 'mosquitto.service'


def _validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart`')


def _validate_and_create_service(action, service) -> str:
    if service.upper() in Services.__members__.keys():
        return f'sudo systemctl {action} {Services[service.upper()].value}'
    else:
        abort(400, message=f'service {service} does not exist in our system`')


class SystemctlCommand(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, help='action should be `start | stop | restart`', required=True)
        parser.add_argument('service',
                            type=str,
                            help='service type is required example: (wires, mosquitto)',
                            required=True)
        args = parser.parse_args()
        action = _validate_and_create_action(args['action'])
        service = _validate_and_create_service(action, args['service'])
        # call = execute_command(service)
        call = True
        if call:
            return {"service": f'{call}, worked!'}
        else:
            return {"service": f'{call}, failed!'}, 404


class SystemctlStatus(Resource):
    @classmethod
    def get(cls, service):
        if service.upper() in Services.__members__.keys():
            check = systemctl_status_check(Services[service.upper()].value)
            if check:
                return {'status': f'{service} is running'}
            else:
                return {'status': f'{service} is not running'}
        else:
            return {'status': f'{service} does not exist in our system'}
