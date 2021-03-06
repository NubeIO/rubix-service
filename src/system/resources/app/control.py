from rubix_http.exceptions.exception import NotFoundException

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.service.control import ServiceControl
from src.system.resources.service.utils import create_service_cmd


class ControlResource(ServiceControl):
    @classmethod
    def validate_and_create_service_cmd(cls, action: str, service: str) -> str:
        try:
            app: InstallableApp = InstallableApp.get_app(service, "")
            return create_service_cmd(action, app.service_file_name)
        except ModuleNotFoundError:
            raise NotFoundException(f'App service {service} does not exist in our system')
