import os

from flask import current_app
from flask_restful import Resource, reqparse, abort

from src import AppSetting
from src.system.apps.base.python_app import PythonApp
from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import download_unzip_service, delete_existing_folder


class DownloadResource(Resource):

    # noinspection DuplicatedCode
    def post(self):
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        app = get_app_from_service(service, version)
        download_dir = app.get_download_dir()
        try:
            name = download_unzip_service(app.get_download_link(), download_dir, app_setting.token)
            downloaded_dir = app.get_downloaded_dir()
            existing_app_deletion = delete_existing_folder(downloaded_dir)
            extracted_dir = os.path.join(download_dir, name)
            if isinstance(app, PythonApp):
                # enforcing to extract on version directory
                dir_with_version = os.path.join(download_dir, version)
                mode = 0o744
                os.makedirs(dir_with_version, mode, True)
                app_file = os.path.join(dir_with_version, 'app')
                os.rename(extracted_dir, app_file)
                os.chmod(app_file, mode)
            else:
                # they are already wrapped on folder
                os.rename(extracted_dir, downloaded_dir)
            return {'service': service, 'version': version, 'existing_app_deletion': existing_app_deletion}
        except Exception as e:
            abort(501, message=str(e))
