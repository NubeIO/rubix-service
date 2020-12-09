import os

from flask_restful import Resource, reqparse, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import delete_existing_folder, download_unzip_service, get_extracted_dir
from src.system.utils.shell_commands import execute_command


class DownloadService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('build_url', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        build_url = args['build_url']
        try:
            app = InstallableApp.get_app(service)
            os.makedirs(app.installation_dir(), 0o775, exist_ok=True)  # create dir if doesn't exist
            if not app.validate_domain(build_url):
                abort(400, message="service {} is an invalid build_url".format(service))
            delete_existing_dir = delete_existing_folder(app.installation_dir())
            download = download_unzip_service(build_url, app.installation_dir())
            if not download:
                abort(501,
                      message="valid URL service {} but download failed check internet or version!".format(service))
            return {'service': service, 'build_url': build_url, 'delete_existing_dir': delete_existing_dir}
        except Exception as e:
            abort(404, message=str(e))


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
        try:
            app = InstallableApp.get_app(service)
            install = execute_command(app.get_install_cmd(user, lib_dir), app.get_cwd())
            if not install:
                abort(400, message="valid service {} issue on install".format(service))
            return {'service': service, 'install completed': install}
        except Exception as e:
            abort(404, message=str(e))


class DeleteInstallation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        try:
            app = InstallableApp.get_app(service)
            delete = execute_command(app.get_delete_command(), app.get_cwd())
            if not delete:
                abort(400, message="valid service {} issue on delete".format(service))
            delete_existing_dir = delete_existing_folder(app.installation_dir())
            return {'service': service, 'delete completed': delete, 'delete_existing_dir': delete_existing_dir}
        except Exception as e:
            abort(404, message=str(e))


class DeleteData(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        try:
            app = InstallableApp.get_app(service)
            delete_data = execute_command(app.get_delete_data_command(), app.get_cwd())
            if not delete_data:
                abort(400, message="valid service {} issue on delete_data".format(service))
            return {'service': service, 'delete_data completed': delete_data}
        except Exception as e:
            abort(404, message=str(e))
