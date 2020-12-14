import os

from flask_restful import Resource, reqparse, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import delete_existing_folder, download_unzip_service, read_file, is_dir_exist, \
    delete_all_folders_except
from src.system.utils.shell_commands import execute_command


class DownloadService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        app: InstallableApp = get_app_from_service(service, version)
        os.makedirs(app.installation_dir(), 0o775, exist_ok=True)  # create dir if doesn't exist
        installation_dir = app.installation_dir()
        try:
            name = download_unzip_service(app.get_download_link(),
                                          installation_dir,
                                          read_file(os.environ.get("token")))
            downloaded_dir = app.get_downloaded_dir()
            existing_app_deletion = delete_existing_folder(downloaded_dir)
            os.rename(os.path.join(installation_dir, name), downloaded_dir)
            return {'service': service, 'version': version, 'existing_app_deletion': existing_app_deletion}
        except Exception as e:
            abort(501, message=str(e))


class InstallService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        user = args['user']
        lib_dir = args['lib_dir']
        app: InstallableApp = get_app_from_service(service, version)
        if not is_dir_exist(app.get_cwd()):
            abort(404, message=str('Please download service {} with version {} at first'.format(service, version)))
        cmd = app.get_install_cmd(user, lib_dir)
        installation = execute_command(cmd, app.get_cwd())
        delete_all_folders_except(app.installation_dir(), version)
        return {'service': service, 'version': version, 'installation': installation}


class DeleteInstallation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        deletion = execute_command(app.get_delete_command(), app.get_cwd())
        existing_apps_deletion = delete_existing_folder(app.installation_dir())
        return {'service': service, 'deletion': deletion, 'existing_apps_deletion': existing_apps_deletion}


class DeleteData(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        deletion = delete_existing_folder(app.get_data_dir())
        return {'service': service, 'deletion': deletion}


def get_app_from_service(service, version='') -> InstallableApp:
    try:
        app = InstallableApp.get_app(service, version)
        return app
    except Exception as e:
        abort(404, message=str(e))
