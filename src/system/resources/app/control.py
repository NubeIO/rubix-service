from flask_restful import abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.service.control import ServiceControl


class ControlResource(ServiceControl):
    @classmethod
    def validate_and_create_service_cmd(cls, action: str, service: str) -> str:
        try:
            app: InstallableApp = InstallableApp.get_app(service, "")
            cmd = ""
            if action == "start":
                cmd = "sudo systemctl enable {} && ".format(app.service_file_name)
            elif action == "stop":
                cmd = "sudo systemctl disable {} && ".format(app.service_file_name)
            return cmd + "sudo systemctl {} {}".format(action, app.service_file_name)
        except ModuleNotFoundError:
            abort(400, message="App service {} does not exist in our system".format(service))
