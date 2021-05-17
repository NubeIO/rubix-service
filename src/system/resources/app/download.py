import gevent
from flask import request, current_app
from rubix_http.exceptions.exception import PreConditionException, NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.system.resources.app.utils import download_async, get_download_state, update_download_state
from src.system.resources.rest_schema.schema_download import download_attributes
from src.system.utils.data_validation import validate_args


class DownloadResource(RubixResource):

    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, download_attributes):
            raise BadDataException('Invalid request')
        if get_download_state().get('downloading', False):
            raise PreConditionException('Download is in progress')
        gevent.spawn(download_async, current_app._get_current_object().app_context, args)
        return {"message": "Download started"}


class DownloadStateResource(RubixResource):

    @classmethod
    def get(cls):
        download_stat = get_download_state()
        if download_stat.get('downloading', False):
            return {'message': 'Download is in progress'}
        services = download_stat.get('services')
        if not services:
            raise NotFoundException('Download state does not exist')
        return services

    @classmethod
    def delete(cls):
        update_download_state({})
        return {'message': 'Download state is cleared'}
