import os

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import delete_existing_folder


class DeleteDataResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        stop: bool = app.stop()
        backup_data: bool = app.backup_data()
        deletion: bool = delete_existing_folder(os.path.join(app.get_global_dir(), 'data'))
        return {'service': service, 'deletion': deletion, 'backup_data': backup_data, 'stop': stop}
