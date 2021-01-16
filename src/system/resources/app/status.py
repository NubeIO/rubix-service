from flask_restful import Resource, abort, fields, marshal_with

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.types import Types
from src.system.systemd.systemd import RubixServiceSystemd
from src.system.utils.file import get_extracted_dir
from src.system.utils.project import get_version
from src.system.utils.shell import systemctl_status


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
        status = systemctl_status(RubixServiceSystemd.SERVICE_FILE_NAME)
        installed_apps.append({
            'version': get_version(),
            'display_name': 'Rubix Service',
            'app_type': Types.INSTALLER.value,
            **status
        })
        for installable_app in inheritors(InstallableApp):
            dummy_app = installable_app()
            version = get_extracted_dir(dummy_app.get_installation_dir())
            if version:
                status = systemctl_status(dummy_app.service_file_name)
                if status:
                    installed_apps.append({
                        'version': version.split("/")[-1],
                        'display_name': dummy_app.display_name,
                        'app_type': dummy_app.app_type,
                        **status
                    })
        return installed_apps
