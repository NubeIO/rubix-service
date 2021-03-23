from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service


class UpdateLoggingResource(RubixResource):
    @classmethod
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        data: str = args['data']
        app: InstallableApp = get_app_from_service(service)
        update = app.update_config_file('logging.conf', data)
        return {'service': service, 'update': update}
