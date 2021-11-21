from rubix_http.exceptions.exception import NotFoundException

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.service.restart_job import ServiceRestartJob
from src.system.resources.service.utils import create_service_cmd


class RestartJobResource(ServiceRestartJob):
    @classmethod
    def validate_and_create_restart_service_cmd(cls, service: str) -> str:
        try:
            app: InstallableApp = InstallableApp.get_app(service, "")
            return create_service_cmd("restart", app.service_file_name)
        except ModuleNotFoundError:
            raise NotFoundException(f'App service {service} does not exist in our system')

    @classmethod
    def validate_service(cls, service: str):
        try:
            InstallableApp.get_app(service, "")
        except ModuleNotFoundError:
            raise NotFoundException(f'App service {service} does not exist in our system')
