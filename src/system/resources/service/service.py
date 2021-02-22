from flask_restful import marshal_with
from rubix_http.resource import RubixResource

from src.system.resources.fields import service_fields
from src.system.resources.service.utils import Services
from src.system.utils.shell import systemctl_status, systemctl_installed


class ServiceResource(RubixResource):
    @classmethod
    @marshal_with(service_fields)
    def get(cls):
        return cls.get_services_stat()

    @classmethod
    def get_services_stat(cls):
        services = []
        for service in Services.__members__.keys():
            services.append(cls.get_service_stat(service))
        return services

    @classmethod
    def get_service_stat(cls, service) -> dict:
        service_file_name: str = Services[service].value.get('service_file_name')
        is_installed: bool = systemctl_installed(service_file_name)
        status: dict = {}
        if is_installed:
            status = systemctl_status(service_file_name)
        return {
            **status,
            'display_name': Services[service].value.get('display_name'),
            'service': service,
            'is_installed': is_installed,
        }
