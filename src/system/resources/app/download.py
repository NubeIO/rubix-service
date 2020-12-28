import os

from flask import current_app
from flask_restful import Resource, reqparse, abort

from src import AppSetting
from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import download_unzip_service, delete_existing_folder


class DownloadResource(Resource):

    def post(self):
        app_setting = current_app.config[AppSetting.KEY]
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
            os.rename(os.path.join(download_dir, name), downloaded_dir)
            return {'service': service, 'version': version, 'existing_app_deletion': existing_app_deletion}
        except Exception as e:
            abort(501, message=str(e))
