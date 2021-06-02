from flask import request
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.system.resources.rest_schema.schema_control import control_attributes
from src.system.resources.service.utils import validate_and_create_action, Services, create_service_cmd
from src.system.utils.data_validation import validate_args
from src.system.utils.shell import execute_command_with_exception


class ServiceControl(RubixResource):
    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, control_attributes):
            raise BadDataException('Invalid request')
        control_res = []
        for arg in args:
            service: str = arg['service']
            action: str = arg['action']
            res = {'service': service, 'action': action, 'error': ''}
            try:
                _action: str = validate_and_create_action(arg['action'])
                service_cmd: str = cls.validate_and_create_service_cmd(_action, arg['service'])
                execute_command_with_exception(service_cmd)
            except Exception as e:
                res = {**res, 'error': str(e)}
            control_res.append(res)
        return control_res

    @classmethod
    def validate_and_create_service_cmd(cls, action: str, service: str) -> str:
        if service in Services.__members__.keys():
            service_file_name = Services[service].value.get('service_file_name')
            return create_service_cmd(action, service_file_name)
        raise NotFoundException(f'service {service} does not exist in our system')
