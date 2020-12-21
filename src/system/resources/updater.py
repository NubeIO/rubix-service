import os

from flask import current_app
from flask_restful import Resource, reqparse, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import delete_existing_folder, download_unzip_service, is_dir_exist, \
    delete_all_folders_except, get_extracted_dir
from src.system.utils.shell_commands import execute_command


class DownloadService(Resource):

    def post(self):
        app_setting = current_app.config['SETTING']
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        app = get_app_from_service(service, version)
        installation_dir = app.get_installation_dir()
        try:
            name = download_unzip_service(app.get_download_link(), installation_dir, app_setting.token)
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
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        lib_dir = args['lib_dir']
        app = get_app_from_service(service, version)
        if not is_dir_exist(app.get_cwd()):
            abort(404, message=str('Please download service {} with version {} at first'.format(service, version)))
        cmd = app.get_install_cmd(lib_dir)
        installation = execute_command(cmd, app.get_cwd())
        delete_all_folders_except(app.get_installation_dir(), version)
        return {'service': service, 'version': version, 'installation': installation}


class DeleteInstallation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app = get_app_from_service(service)
        # TODO: when we have DB to store installed version, we don't need to do this
        version = get_extracted_dir(app.get_installation_dir())
        if not version:
            abort(404, message="service {} is not running".format(service))
        app.set_version(version)
        deletion = execute_command(app.get_delete_command(), app.get_cwd())
        existing_apps_deletion = delete_existing_folder(app.get_installation_dir())
        return {'service': service, 'deletion': deletion, 'existing_apps_deletion': existing_apps_deletion}


class DeleteData(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app = get_app_from_service(service)
        deletion = delete_existing_folder(app.get_data_dir())
        return {'service': service, 'deletion': deletion}


def get_app_from_service(service, version='') -> InstallableApp:
    try:
        app = InstallableApp.get_app(service, version)
        return app
    except Exception as e:
        abort(404, message=str(e))
