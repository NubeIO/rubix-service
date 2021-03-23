import json

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service


class UpdateConfigResource(RubixResource):
    @classmethod
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=dict, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        data: dict = args['data']
        app: InstallableApp = get_app_from_service(service)
        json_data = json.dumps(data, indent=2)
        update = app.update_config_file('config.json', json_data)
        return {'service': service, 'update': update}
