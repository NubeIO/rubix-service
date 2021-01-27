from flask_restful import Resource, abort, fields, marshal_with

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_installed_app_details
from src.system.resources.fields import service_fields
from src.system.utils.shell import systemctl_installed


class AppResource(Resource):
    fields = {
        'version': fields.String,
        'app_type': fields.String,
        'gateway_access': fields.Boolean,
        'min_support_version': fields.String,
        'port': fields.Integer,
        **service_fields
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
                return {**details, 'is_installed': True}
        return {**app.to_property_dict(), 'service': app.service(), 'is_installed': False}
