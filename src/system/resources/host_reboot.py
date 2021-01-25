from flask_restful import Resource, reqparse, abort

from src.system.resources.service.utils import validate_host_restart
from src.system.utils.shell import execute_command_with_exception


class HostReboot(Resource):
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
        try:
            execute_command_with_exception(service)
            return {}
        except Exception as e:
            abort(501, message=str(e))
