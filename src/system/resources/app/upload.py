from flask_restful import reqparse
from packaging.version import Version
from rubix_http.exceptions.exception import PreConditionException, BadDataException
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
        match: bool = Version._regex.search(version)
        if not match:
            raise BadDataException(f'Invalid version, version needs to be like v1.0.0, v1.1.0')
        app: InstallableApp = get_app_from_service(service, version)
        return app.upload(file)
