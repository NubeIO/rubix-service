import os

from flask_restful import Resource, reqparse, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import delete_existing_folder, download_unzip_service, read_file
from src.system.utils.shell_commands import execute_command


class DownloadService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('build_url', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        build_url = args['build_url']
        app: InstallableApp = get_app_from_service(service)
        os.makedirs(app.installation_dir(), 0o775, exist_ok=True)  # create dir if doesn't exist
        valid = app.validate_domain(build_url)
        if not valid:
            abort(404, message=f"service {service} is an invalid build_url")
        delete_existing_dir = delete_existing_folder(app.installation_dir())
        download = download_unzip_service(build_url, app.installation_dir(), read_file(os.environ.get("token")))
        if not download:
            abort(501, message="valid URL service {} but download failed check internet or version!".format(service))
        return {'service': service, 'build_url': build_url, 'delete_existing_dir': delete_existing_dir}


class InstallService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        user = args['user']
        lib_dir = args['lib_dir']
        app: InstallableApp = get_app_from_service(service)
        try:
            cmd = app.get_install_cmd(user, lib_dir)  # may got failed on evaluating wd
        except Exception as e:
            abort(400, message=str(e))
            return
        install = execute_command_and_handle_error(cmd, app)
        return {'service': service, 'install completed': install}


class DeleteInstallation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete = execute_command_and_handle_error(app.get_delete_command(), app)
        delete_existing_dir = delete_existing_folder(app.installation_dir())
        return {'service': service, 'delete completed': delete, 'delete_existing_dir': delete_existing_dir}


class DeleteData(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete_data = delete_existing_folder(app.get_data_dir())
        return {'service': service, 'delete_data completed': delete_data}


def get_app_from_service(service) -> InstallableApp:
    try:
        app = InstallableApp.get_app(service)
        return app
    except Exception as e:
        abort(404, message=str(e))


def execute_command_and_handle_error(cmd, app: InstallableApp) -> bool:
    try:
        cwd = app.get_cwd()
        return execute_command(cmd, cwd)
    except Exception as e:
        abort(400, message=str(e))
