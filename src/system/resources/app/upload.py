from flask_restful import reqparse
from rubix_http.exceptions.exception import PreConditionException
from rubix_http.resource import RubixResource
from werkzeug.datastructures import FileStorage

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service


class UploadResource(RubixResource):

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        parser.add_argument('file', type=FileStorage, location='files', required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        version = args['version']
        file = args['file']
        if file.filename.split('.')[-1] != 'zip':
            raise PreConditionException(f'File must be in zip format')
        if version[1:] not in file.filename:
            raise PreConditionException(f'File {file.filename} version mismatch with version {version}')
        app: InstallableApp = get_app_from_service(service, version)
        return app.upload(file)
