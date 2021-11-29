from flask import request
from rubix_http.exceptions.exception import BadDataException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.resources.rest_schema.schema_delete_data import delete_data_attributes
from src.system.utils.data_validation import validate_args
from src.system.utils.file import delete_existing_folder


class DeleteDataResource(RubixResource):
    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, delete_data_attributes):
            raise BadDataException('Invalid request')
        delete_data_res = []
        for arg in args:
            service: str = arg['service'].upper()
            app: InstallableApp = get_app_from_service(service)
            try:
                res = {'service': service, 'deletion': False, 'backup_data': False, 'stop': False, 'error': ''}
                stop: bool = app.stop()
                backup_data: bool = app.backup_data()
                deletion: bool = delete_existing_folder(app.get_data_dir())
                res = {**res, 'deletion': deletion, 'backup_data': backup_data, 'stop': stop}
            except Exception as e:
                res = {'error': str(e)}
            delete_data_res.append(res)
        return delete_data_res
