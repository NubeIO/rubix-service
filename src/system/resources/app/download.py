from flask_restful import Resource, reqparse, abort

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service


class DownloadResource(Resource):

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        app: InstallableApp = get_app_from_service(service, version)
        try:
            return app.download()
        except Exception as e:
            abort(501, message=str(e))
