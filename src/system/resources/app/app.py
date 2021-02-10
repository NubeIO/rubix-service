from flask import current_app
from flask_restful import Resource, abort, fields, marshal_with
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_installed_app_details, get_app_from_service
from src.system.resources.fields import service_fields
from src.system.utils.shell import systemctl_installed

logger = LocalProxy(lambda: current_app.logger)


class AppResource(Resource):
    fields = {
        'version': fields.String,
        'app_type': fields.String,
        'gateway_access': fields.Boolean,
        'min_support_version': fields.String,
        'port': fields.Integer,
        **service_fields,
        'name': fields.String,
        'created_at': fields.String,
        'browser_download_url': fields.String,
        'latest_version': fields.String
    }

    @classmethod
    @marshal_with(fields)
    def get(cls):
        try:
            return cls.get_installed_apps_stat()
        except Exception as e:
            abort(501, message=str(e))

    @classmethod
    def get_installed_apps_stat(cls):
        installed_apps = []
        for installable_app in inheritors(InstallableApp):
            installed_apps.append(cls.get_installed_app_stat(installable_app()))
        return installed_apps

    @classmethod
    def get_installed_app_stat(cls, app: InstallableApp) -> dict:
        if systemctl_installed(app.service_file_name):
            details: dict = get_installed_app_details(app)
            if details:
                app = get_app_from_service(details['service'], details['version'])
                app_setting = current_app.config[AppSetting.FLASK_KEY]
                browser_download_url = {}
                latest_version = None
                try:
                    browser_download_url = app.get_download_link(app_setting.token, True)
                except Exception as e:
                    logger.error(str(e))
                try:
                    latest_version = app.get_latest_release(app_setting.token)
                except Exception as e:
                    logger.error(str(e))
                return {**details, 'is_installed': True, **browser_download_url, 'latest_version': latest_version}
        return {**app.to_property_dict(), 'service': app.service(), 'is_installed': False}
