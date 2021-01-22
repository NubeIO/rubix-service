from flask_restful import Resource, abort, fields, marshal_with

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types
from src.system.resources.app.utils import get_installed_app_details
from src.system.utils.project import get_version
from src.system.utils.shell import systemctl_status


class StatusResource(Resource):
    fields = {
        'version': fields.String,
        'display_name': fields.String,
        'app_type': fields.String,
        'service': fields.String,
        'service_file': fields.String,
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
        # TODO: we will remove out from here and will depend on ping
        status = systemctl_status('nubeio-rubix-service.service')
        installed_apps.append({
            'version': get_version(),
            'display_name': 'Rubix Service',
            'app_type': Types.INSTALLER.value,
            **status
        })
        for installable_app in inheritors(InstallableApp):
            dummy_app = installable_app()
            details = get_installed_app_details(dummy_app)
            if details:
                installed_apps.append(details)
        return installed_apps
