from flask_restful import Resource, reqparse, marshal_with, fields

from src.system.resources.service.utils import validate_and_create_action, validate_and_create_service
from src.system.utils.shell_commands import execute_command


class SystemctlCommand(Resource):
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
                            help='action should be `start | stop | restart | disable | enable`',
                            required=True)
        parser.add_argument('service',
                            type=str,
                            help='service type is required example: (wires, mosquitto)',
                            required=True)
        args = parser.parse_args()
        action = validate_and_create_action(args['action'])
        service = validate_and_create_service(action, args['service'])
        call = execute_command(service)
        if call:
            msg = "success: {}".format(service)
            return {'msg': msg, 'status': True}
        msg = "failed: {}".format(service)
        return {'msg': msg, 'status': False}
