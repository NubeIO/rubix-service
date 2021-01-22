from flask_restful import Resource, reqparse, marshal_with, fields
from src.system.resources.service.utils import validate_host_restart
from src.system.utils.shell import execute_command


class HostReboot(Resource):
    fields = {
        'msg': fields.String,
        'status': fields.Boolean,
    }

    @classmethod
    @marshal_with(fields)
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('action',
                            type=str,
                            help='action should be `restart`',
                            required=True)
        args = parser.parse_args()
        action = args['action']
        service = validate_host_restart(action)
        call = execute_command(service)
        if call:
            msg = "success: {}".format(service)
            return {'msg': msg, 'status': True}
        msg = "failed: {}".format(service)
        return {'msg': msg, 'status': False}
