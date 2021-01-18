from flask_restful import Resource, marshal_with, fields

from src.system.resources.service.utils import validate_service
from src.system.utils.shell import systemctl_status_check


class SystemctlStatusBool(Resource):
    fields = {
        'msg': fields.String,
        'status': fields.Boolean,
    }

    @classmethod
    @marshal_with(fields)
    def get(cls, service):
        service = service.upper()
        service_name = validate_service(service)
        if service_name:
            status_check = systemctl_status_check(service_name)
            if status_check:
                msg = "{} is running".format(service)
                return {'msg': msg, 'status': True}
            else:
                msg = "{} is not running".format(service)
                return {'msg': msg, 'status': False}
        msg = "{} does not exist in our system".format(service)
        return {'msg': msg, 'status': False}
