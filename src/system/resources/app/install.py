import gevent
from flask import request, current_app
from rubix_http.exceptions.exception import PreConditionException, BadDataException
from rubix_http.resource import RubixResource

from src.system.apps.enums.enums import DownloadState
from src.system.resources.app.utils import get_download_state, install_app, install_app_async
from src.system.resources.rest_schema.schema_install import install_attributes
from src.system.utils.data_validation import validate_args


class InstallResource(RubixResource):
    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, install_attributes):
            raise BadDataException('Invalid request')
        download_state: str = get_download_state().get('state')
        if download_state == DownloadState.DOWNLOADING.name:
            raise PreConditionException('Download is in progress')
        elif download_state == DownloadState.DOWNLOADED.name:
            raise PreConditionException('Download state is not cleared')
        install_res = []
        rubix_plat = args.pop(next((i for i, item in enumerate(args) if item["service"].upper() == "RUBIX_PLAT"), -1))
        processes = []
        for arg in args:
            processes.append(gevent.spawn(install_app_async, current_app._get_current_object().app_context, arg))
        gevent.joinall(processes)
        for process in processes:
            install_res.append(process.value)
        if rubix_plat:
            install_res.append(install_app(rubix_plat))
        return install_res
