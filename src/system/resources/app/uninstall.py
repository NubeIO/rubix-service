from flask_restful import Resource, reqparse, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import get_extracted_dir, delete_existing_folder


class UnInstallResource(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        version: str = get_extracted_dir(app.get_installation_dir())
        if not version:
            abort(404, message="service {} is not running".format(service))
        try:
            app.set_version(version)
            deletion: bool = app.uninstall()
            existing_apps_deletion: bool = delete_existing_folder(app.get_installation_dir())
            return {'service': service, 'deletion': deletion, 'existing_apps_deletion': existing_apps_deletion}
        except Exception as e:
            abort(501, message=str(e))
