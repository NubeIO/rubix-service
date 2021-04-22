from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service


class InstallResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        version: str = args['version']
        app: InstallableApp = get_app_from_service(service, version)
        return app.install_app()
