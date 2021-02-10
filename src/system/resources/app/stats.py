from flask_restful import Resource, marshal_with, abort, reqparse, inputs

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.app import AppResource


class AppStatsResource(Resource):
    @classmethod
    @marshal_with(AppResource.fields)
    def get(cls, service):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('browser_download_url', type=inputs.boolean, default=False)
            parser.add_argument('latest_version', type=inputs.boolean, default=False)
            args = parser.parse_args()
            browser_download_url = args['browser_download_url']
            latest_version = args['latest_version']
            app: InstallableApp = InstallableApp.get_app(service, None)
            return AppResource.get_installed_app_stat(app, browser_download_url, latest_version)
        except ModuleNotFoundError as e:
            abort(404, message=str(e))
        except Exception as e:
            abort(501, message=str(e))
