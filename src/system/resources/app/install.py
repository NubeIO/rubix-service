import shutil

from flask_restful import Resource, reqparse, abort

from src.system.apps.base.frontend_app import FrontendApp
from src.system.apps.base.python_app import PythonApp
from src.system.resources.app.utils import get_app_from_service
from src.system.systemd.systemd import AppSystemd
from src.system.utils.file import is_dir_exist, delete_existing_folder
from src.system.utils.shell import execute_command


class InstallResource(Resource):
    # noinspection DuplicatedCode
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        app = get_app_from_service(service, version)
        if not is_dir_exist(app.get_downloaded_dir()):
            abort(404, message=str('Please download service {} with version {} at first'.format(service, version)))
        delete_existing_folder(app.get_installation_dir())
        shutil.copytree(app.get_downloaded_dir(), app.get_installed_dir())
        installation = False
        if isinstance(app, PythonApp):
            systemd = AppSystemd(app.service_file_name, app.pre_start_sleep, app.get_wd(), app.port, app.get_data_dir(),
                                 app.repo_name, app.description)
            installation = systemd.install()
        elif isinstance(app, FrontendApp):
            installation = execute_command(app.get_install_cmd(), app.get_cwd())
        delete_existing_folder(app.get_download_dir())
        return {'service': service, 'version': version, 'installation': installation}
