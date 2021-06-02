import os
from datetime import datetime

from flask import send_file
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException, BadDataException, NotImplementedException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import is_dir_exist


class DownloadDataResource(RubixResource):
    @classmethod
    def get(cls):
        service: str = request.args.get('service')
        if not service:
            raise BadDataException("Include ?service as an argument")
        app: InstallableApp = get_app_from_service(service)
        if not is_dir_exist(os.path.join(app.get_global_dir(), 'data')):
            raise NotFoundException(f'Service {service} does not have any data to download')
        file = app.download_data()
        if request.args.get('bridge'):
            raise NotImplementedException("We don't have the application/zip download support yet!")
        return send_file(file,
                         mimetype='application/zip',
                         attachment_filename=f'{service}_DATA_{datetime.now().strftime("%Y%m%d%H%M%S")}.zip',
                         as_attachment=True)
