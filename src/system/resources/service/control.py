from flask_restful import Resource, reqparse, abort

from src.system.resources.service.utils import validate_and_create_action, Services
from src.system.utils.shell import execute_command_with_exception


class ServiceControl(Resource):
    @classmethod
    def post(cls):
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
        action: str = validate_and_create_action(args['action'])
        service_cmd: str = cls.validate_and_create_service_cmd(action, args['service'])
        try:
            execute_command_with_exception(service_cmd)
            return {}
        except Exception as e:
            abort(501, message=str(e))

    @classmethod
    def validate_and_create_service_cmd(cls, action: str, service: str) -> str:
        if service in Services.__members__.keys():
            service_file_name = Services[service].value.get('service_file_name')
            return "sudo systemctl {} {}".format(action, service_file_name)
        abort(400, message="service {} does not exist in our system".format(service))
