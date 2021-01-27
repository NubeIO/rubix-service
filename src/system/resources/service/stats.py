from flask_restful import Resource, marshal_with, abort

from src.system.resources.fields import service_fields
from src.system.resources.service.service import ServiceResource
from src.system.resources.service.utils import validate_service


class ServiceStats(Resource):
    @classmethod
    @marshal_with(service_fields)
    def get(cls, service):
        validate_service(service)
        try:
            return ServiceResource.get_service_stat(service)
        except Exception as e:
            return abort(501, message=str(e))
