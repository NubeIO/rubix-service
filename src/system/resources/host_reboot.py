from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.system.resources.service.utils import validate_host_restart
from src.system.utils.shell import execute_command_with_exception


class HostReboot(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('action',
                            type=str,
                            help='action should be `restart`',
                            required=True)
        args = parser.parse_args()
        action = args['action']
        service = validate_host_restart(action)
        execute_command_with_exception(service)
        return {}
