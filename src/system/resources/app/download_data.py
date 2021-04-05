import os
from datetime import datetime

from flask import send_file
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import is_dir_exist


class DownloadDataResource(RubixResource):
    @classmethod
    def get(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        if not is_dir_exist(os.path.join(app.get_global_dir(), 'data')):
            raise NotFoundException(f'Service {service.upper()} does not have any data to download')
        file = app.download_data()
        return send_file(file,
                         attachment_filename=f'{service.upper()}_DATA_{datetime.now().strftime("%Y%m%d%H%M%S")}',
                         as_attachment=True)
