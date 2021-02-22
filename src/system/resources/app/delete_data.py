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
        deletion: bool = delete_existing_folder(app.get_data_dir())
        restart: bool = app.restart()
        return {'service': service, 'deletion': deletion, 'restart': restart}
