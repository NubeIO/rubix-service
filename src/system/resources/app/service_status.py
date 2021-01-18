from flask_restful import Resource, marshal_with, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.status import StatusResource
from src.system.resources.app.utils import get_installed_app_details


class ServiceStatusResource(Resource):
    @classmethod
    @marshal_with(StatusResource.fields)
    def get(cls, service):
        try:
            service = service.upper()
            app = InstallableApp.get_app(service, None)
            details = get_installed_app_details(app)
            if details:
                return details
            else:
                raise ModuleNotFoundError("service {} is not installed".format(service))
        except ModuleNotFoundError as e:
            abort(404, message=str(e))
        except Exception as e:
            abort(501, message=str(e))
