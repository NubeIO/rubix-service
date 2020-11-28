import enum
from flask_restful import Resource, reqparse, abort

from src.system.resources.systemctl_services import ServiceAction
from src.system.services import Services
from src.system.utils.shell_commands import execute_command, systemctl_status_check, systemctl_status

'''
HTTP get and show options
stop existing service RETURN 200 or 404
## delete existing RETURN 200 or 404
## unzip RETURN 200 or 404
## start install RETURN 200 or 404

'''


def download_service(service):
    return service


def stop_service(service):
    return service


def delete_existing_folder(service):
    return service


def unzip_service(service):
    return service


def install_service(service):
    return service


def restart_service(service):
    return service


def check_service_is_running(service):
    return service


def _validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart`')


def _validate_and_create_service(action, service) -> str:
    if service.upper() in Services.__members__.keys():
        return "sudo systemctl {} {}".format(action, Services[service.upper()].value)
    else:
        abort(400, message="service {} does not exist in our system".format(service))


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
        if service.upper() in Services.__members__.keys():
            check = systemctl_status_check(Services[service.upper()].value)
            if check:
                msg = "status: {} is running".format(service)
                return {'msg': msg, 'status': True, 'fail': False}
            else:
                msg = "status: {} is not running".format(service)
                return {'msg': msg, 'status': False, 'fail': False}
        else:
            msg = "status: {}  does not exist in our system".format(service)
            return {'msg': msg, 'status': False, 'fail': True}


class SystemctlStatus(Resource):
    @classmethod
    def get(cls, service):
        if service.upper() in Services.__members__.keys():
            check = systemctl_status(Services[service.upper()].value)
            if check:
                msg = check
                return {'msg': msg, 'status': True, 'fail': False}
        else:
            msg = "status: {}  does not exist in our system".format(service)
            return {'msg': msg, 'status': False, 'fail': True}
