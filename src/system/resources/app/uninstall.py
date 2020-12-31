from flask_restful import Resource, reqparse, abort

from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import get_extracted_dir, delete_existing_folder
from src.system.utils.shell import execute_command


class UnInstallResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app = get_app_from_service(service)
        version = get_extracted_dir(app.get_installation_dir())
        if not version:
            abort(404, message="service {} is not running".format(service))
        app.set_version(version)
        deletion = execute_command(app.get_delete_command(), app.get_cwd())
        existing_apps_deletion = delete_existing_folder(app.get_installation_dir())
        return {'service': service, 'deletion': deletion, 'existing_apps_deletion': existing_apps_deletion}
