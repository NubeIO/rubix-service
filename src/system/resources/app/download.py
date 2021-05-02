import gevent
from flask import request, current_app
from rubix_http.exceptions.exception import PreConditionException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.resources.rest_schema.schema_download import download_attributes
from src.system.utils.data_validation import validate_args


class DownloadResource(RubixResource):

    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, download_attributes):
            raise PreConditionException('Invalid request.')
        processes = []
        install_res = []
        for arg in args:
            service = arg['service'].upper()
            version = arg['version']
            app: InstallableApp = get_app_from_service(service, version)
            processes.append(gevent.spawn(app.download_async, current_app._get_current_object().app_context))
        gevent.joinall(processes)
        for process in processes:
            install_res.append(process.value)
        return install_res
