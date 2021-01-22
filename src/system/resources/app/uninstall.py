from flask_restful import Resource, reqparse, abort

from src.system.apps.base.frontend_app import FrontendApp
from src.system.apps.base.python_app import PythonApp
from src.system.resources.app.utils import get_app_from_service
from src.system.systemd.systemd import AppSystemd
from src.system.utils.file import get_extracted_dir, delete_existing_folder


class UnInstallResource(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app = get_app_from_service(service)
        version = get_extracted_dir(app.get_installation_dir())
        if not version:
            abort(404, message="service {} is not running".format(service))
        deletion = False
        if isinstance(app, PythonApp):
            app_creator = AppSystemd(app.service_file_name)
            deletion = app_creator.uninstall()
        elif isinstance(app, FrontendApp):
            app.set_version(version)
            deletion = app.execute_uninstall()
        existing_apps_deletion = delete_existing_folder(app.get_installation_dir())
        return {'service': service, 'deletion': deletion, 'existing_apps_deletion': existing_apps_deletion}
