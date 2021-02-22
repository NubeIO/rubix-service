from flask_restful import marshal_with
from rubix_http.resource import RubixResource

from src.system.resources.fields import service_fields
from src.system.resources.service.service import ServiceResource
from src.system.resources.service.utils import validate_service


class ServiceStats(RubixResource):
    @classmethod
    @marshal_with(service_fields)
    def get(cls, service):
        validate_service(service)
        return ServiceResource.get_service_stat(service)
