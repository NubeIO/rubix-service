from flask_restful import Resource, marshal_with, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.app import AppResource


class AppStatsResource(Resource):
    @classmethod
    @marshal_with(AppResource.fields)
    def get(cls, service):
        try:
            app: InstallableApp = InstallableApp.get_app(service, None)
            return AppResource.get_installed_app_stat(app)
        except ModuleNotFoundError as e:
            abort(404, message=str(e))
        except Exception as e:
            abort(501, message=str(e))
