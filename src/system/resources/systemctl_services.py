import enum
from flask_restful import Resource, reqparse, abort
from src.system.services import Services, validate_service
from src.system.utils.shell_commands import execute_command, systemctl_status_check, systemctl_status


class ServiceAction(enum.Enum):
    START = 1
    STOP = 2
    RESTART = 3
    DISABLE = 4
    ENABLE = 5


def _validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart | disable | enable`')


def _validate_and_create_service(action, service) -> str:
    service = service.upper()
    if validate_service(service):
        return "sudo systemctl {} {}".format(action, Services[service.upper()].value)
    else:
        abort(400, message="service {} does not exist in our system".format(service))


class SystemctlCommand(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action',
                            type=str,
                            help='action should be `start | stop | restart | disable | enable`',
                            required=True)
        parser.add_argument('service',
                            type=str,
                            help='service type is required example: (wires, mosquitto)',
                            required=True)
        args = parser.parse_args()
        action = _validate_and_create_action(args['action'])
        service = _validate_and_create_service(action, args['service'])
        call = execute_command(service)
        if call:
            msg = "update to service success: {}".format(service)
            return {'msg': msg, 'status': True, 'fail': False}
        else:
            msg = "update to service failed: {}".format(service)
            return {'msg': msg, 'status': False, 'fail': False}, 404


class SystemctlStatusBool(Resource):
    @classmethod
    def get(cls, service):
        service = service.upper()
        if validate_service(service):
            check = systemctl_status_check(Services[service.upper()].value)
            if check:
                msg = f"status: {service} is running"
                return {'msg': msg, 'status': True, 'fail': False}
            else:
                msg = f"status: {service} is not running"
                return {'msg': msg, 'status': False, 'fail': False}
        else:
            msg = f"status: {service} does not exist in our system"
            return {'msg': msg, 'status': False, 'fail': True}


class SystemctlStatus(Resource):
    @classmethod
    def get(cls, service):
        service = service.upper()
        if validate_service(service):
            check = systemctl_status(Services[service.upper()].value)
            if check:
                msg = check
                return {'msg': msg, 'status': True, 'fail': False}
        else:
            msg = f"status: {service} does not exist in our system"
            return {'msg': msg, 'status': False, 'fail': True}
