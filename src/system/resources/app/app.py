from flask import current_app
from flask_restful import fields, marshal_with, reqparse, inputs
from rubix_http.resource import RubixResource
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_installed_app_details, get_app_from_service
from src.system.resources.fields import service_fields
from src.system.utils.shell import systemctl_installed

logger = LocalProxy(lambda: current_app.logger)


class AppResource(RubixResource):
    fields = {
        'version': fields.String,
        'app_type': fields.String,
        'gateway_access': fields.Boolean,
        'min_support_version': fields.String,
        'port': fields.Integer,
        **service_fields,
        'browser_download_url': fields.String,
        'latest_version': fields.String
    }

    @classmethod
    @marshal_with(fields)
    def get(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('browser_download_url', type=inputs.boolean, default=False)
        parser.add_argument('latest_version', type=inputs.boolean, default=False)
        args = parser.parse_args()
        browser_download_url: bool = args['browser_download_url']
        latest_version: bool = args['latest_version']
        return cls.get_installed_apps_stat(browser_download_url, latest_version)

    @classmethod
    def get_installed_apps_stat(cls, browser_download_url: bool, latest_version: bool):
        installed_apps = []
        for installable_app in inheritors(InstallableApp):
            installed_apps.append(cls.get_installed_app_stat(installable_app(), browser_download_url, latest_version))
        return installed_apps

    @classmethod
    def get_installed_app_stat(cls, app: InstallableApp, browser_download_url: bool, latest_version: bool) -> dict:
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        _latest_version = None
        if latest_version:
            try:
                _latest_version = app.get_latest_release(app_setting.token)
            except Exception as e:
                logger.error(str(e))
        if systemctl_installed(app.service_file_name):
            details: dict = get_installed_app_details(app)
            if details:
                app: InstallableApp = get_app_from_service(details['service'])
                app.set_version(details['version'])
                _browser_download_url = {}
                if browser_download_url:
                    try:
                        _browser_download_url = app.get_download_link(app_setting.token, True)
                    except Exception as e:
                        logger.error(str(e))
                return {
                    **details,
                    'is_installed': True,
                    **_browser_download_url,
                    'latest_version': _latest_version
                }
        return {
            **app.to_property_dict(),
            'service': app.service(),
            'is_installed': False,
            'latest_version': _latest_version
        }
