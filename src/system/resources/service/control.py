from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.system.resources.service.utils import validate_and_create_action, Services, create_service_cmd
from src.system.utils.shell import execute_command_with_exception


class ServiceControl(RubixResource):
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
        execute_command_with_exception(service_cmd)
        return {}

    @classmethod
    def validate_and_create_service_cmd(cls, action: str, service: str) -> str:
        if service in Services.__members__.keys():
            service_file_name = Services[service].value.get('service_file_name')
            return create_service_cmd(action, service_file_name)
        raise NotFoundException(f'service {service} does not exist in our system')
