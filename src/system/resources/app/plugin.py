import gevent
from flask import request, current_app
from rubix_http.exceptions.exception import BadDataException, NotFoundException, PreConditionException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.enums import DownloadState
from src.system.resources.app.utils import get_github_token, download_plugins_async, get_app_from_service, \
    get_plugin_download_state, update_plugin_download_state
from src.system.resources.rest_schema.schema_download import download_plugin_attributes
from src.system.resources.rest_schema.schema_install import install_plugin_attributes
from src.system.utils.data_validation import validate_args


class PluginResource(RubixResource):
    @classmethod
    def get(cls, service):
        token: str = get_github_token()
        app: InstallableApp = get_app_from_service(service)
        _version: str = app.get_installed_version()
        if not _version:
            return {"message": f"Please install service {service} first"}
        app.set_version(_version)
        return app.get_plugin_list(token)


class DownloadPluginResource(RubixResource):
    @classmethod
    def post(cls, service):
        args = request.get_json()
        if not validate_args(args, download_plugin_attributes):
            raise BadDataException('Invalid request')
        download_state: str = get_plugin_download_state().get('state')
        if download_state == DownloadState.DOWNLOADING.name:
            raise PreConditionException('Download is in progress')
        elif download_state == DownloadState.DOWNLOADED.name:
            raise PreConditionException('Download state is not cleared')
        app: InstallableApp = get_app_from_service(service.upper())
        _version: str = app.get_installed_version()
        if not _version:
            return {"message": f"Please install service {service} first"}
        app.set_version(_version)
        update_plugin_download_state(DownloadState.DOWNLOADING)
        gevent.spawn(download_plugins_async, current_app._get_current_object().app_context, app, args)
        return {"message": "Download started"}


class PluginDownloadStateResource(RubixResource):

    @classmethod
    def get(cls):
        return get_plugin_download_state()

    @classmethod
    def delete(cls):
        update_plugin_download_state(DownloadState.CLEARED)
        return {'message': 'Download state is cleared'}


class InstallPluginResource(RubixResource):
    @classmethod
    def post(cls, service):
        args = request.get_json()
        if not validate_args(args, install_plugin_attributes):
            raise BadDataException('Invalid request')
        install_res = []
        try:
            app: InstallableApp = get_app_from_service(service)
            _version: str = app.get_installed_version()
            if not _version:
                return {"message": f"Please install service {service} first"}
            for arg in args:
                plugin: str = arg["plugin"].lower()
                installation = app.install_plugin(plugin)
                install_res.append({'plugin': plugin, 'installation': installation, 'error': ''})
        except (Exception, NotFoundException) as e:
            raise NotFoundException(str(e))
        return install_res


class UnInstallPluginResource(RubixResource):
    @classmethod
    def post(cls, service):
        args = request.get_json()
        if not validate_args(args, install_plugin_attributes):
            raise BadDataException('Invalid request')
        uninstall_res = []
        try:
            app: InstallableApp = get_app_from_service(service)
            for arg in args:
                plugin: str = arg["plugin"].lower()
                installation = app.uninstall_plugin(plugin)
                uninstall_res.append({'plugin': plugin, 'uninstall': installation, 'error': ''})
        except (Exception, NotFoundException) as e:
            raise NotFoundException(str(e))
        return uninstall_res
