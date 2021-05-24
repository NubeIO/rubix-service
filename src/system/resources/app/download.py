import gevent
from flask import request, current_app
from rubix_http.exceptions.exception import PreConditionException, BadDataException
from rubix_http.resource import RubixResource

from src.system.apps.enums.enums import DownloadState
from src.system.resources.app.utils import download_async, get_download_state, update_download_state
from src.system.resources.rest_schema.schema_download import download_attributes
from src.system.utils.data_validation import validate_args


class DownloadResource(RubixResource):

    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, download_attributes):
            raise BadDataException('Invalid request')
        download_state: str = get_download_state().get('state')
        if download_state == DownloadState.DOWNLOADING.name:
            raise PreConditionException('Download is in progress')
        elif download_state == DownloadState.DOWNLOADED.name:
            raise PreConditionException('Download state is not cleared')
        update_download_state(DownloadState.DOWNLOADING)
        gevent.spawn(download_async, current_app._get_current_object().app_context, args)
        return {"message": "Download started"}


class DownloadStateResource(RubixResource):

    @classmethod
    def get(cls):
        return get_download_state()

    @classmethod
    def delete(cls):
        update_download_state(DownloadState.CLEARED)
        return {'message': 'Download state is cleared'}
