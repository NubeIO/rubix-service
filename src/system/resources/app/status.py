from flask_restful import Resource, abort, fields, marshal_with

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_installed_app_details


class StatusResource(Resource):
    fields = {
        'version': fields.String,
        'display_name': fields.String,
        'app_type': fields.String,
        'service': fields.String,
        'state': fields.String,
        'status': fields.Boolean,
        'date_since': fields.String,
        'time_since': fields.String,
    }

    @classmethod
    @marshal_with(fields)
    def get(cls):
        try:
            return cls.get_installed_apps()
        except Exception as e:
            abort(501, message=str(e))

    @classmethod
    def get_installed_apps(cls):
        installed_apps = []
        # TODO: have this one after self update integration
        # status = systemctl_status(RubixServiceSystemd.SERVICE_FILE_NAME)
        # installed_apps.append({
        #     'version': get_version(),
        #     'display_name': 'Rubix Service',
        #     'app_type': Types.INSTALLER.value,
        #     **status
        # })
        for installable_app in inheritors(InstallableApp):
            dummy_app = installable_app()
            details = get_installed_app_details(dummy_app)
            if details:
                installed_apps.append(details)
        return installed_apps
