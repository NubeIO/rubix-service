from flask_restful import Resource, marshal_with, fields

from src.system.resources.service.utils import validate_service
from src.system.utils.shell_commands import systemctl_status


class SystemctlStatus(Resource):
    fields = {
        'service': fields.String,
        'msg': fields.String,
        'status': fields.Boolean,
        'date_since': fields.String,
        'time_since': fields.String,
    }

    @classmethod
    @marshal_with(fields)
    def get(cls, service):
        service = service.upper()
        service_name = validate_service(service)
        if service_name:
            try:
                status = systemctl_status(service_name)
                if status:
                    return {**status}
                else:
                    msg = "{} is not running".format(service)
                    return {'msg': msg, 'status': False}
            except Exception as e:
                return {'msg': str(e), 'status': False}
        msg = "{} does not exist in our system".format(service)
        return {'msg': msg, 'status': False}
