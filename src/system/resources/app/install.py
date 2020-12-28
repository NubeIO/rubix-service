import shutil

from flask_restful import Resource, reqparse, abort

from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import is_dir_exist, delete_existing_folder
from src.system.utils.shell_commands import execute_command


class InstallResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        lib_dir = args['lib_dir']
        app = get_app_from_service(service, version)
        if not is_dir_exist(app.get_downloaded_dir()):
            abort(404, message=str('Please download service {} with version {} at first'.format(service, version)))
        delete_existing_folder(app.get_installation_dir())
        shutil.copytree(app.get_downloaded_dir(), app.get_installed_dir())
        cmd = app.get_install_cmd(lib_dir)
        installation = execute_command(cmd, app.get_cwd())
        delete_existing_folder(app.get_download_dir())
        return {'service': service, 'version': version, 'installation': installation}
