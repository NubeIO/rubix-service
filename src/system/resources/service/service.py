from flask_restful import Resource, marshal_with, fields, abort

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.constants.types import OTHERS
from src.system.resources.service.utils import Services
from src.system.utils.shell import systemctl_status


class ServiceResource(Resource):
    fields = {
        'display_name': fields.String,
        'app_type': fields.String,
        'installable': fields.Boolean,
        'service': fields.String,
        'state': fields.String,
        'status': fields.Boolean,
        'date_since': fields.String,
        'time_since': fields.String,
    }

    @classmethod
    @marshal_with(fields)
    def get(cls):
        services = []
        try:
            return cls.get_services(services)
        except Exception as e:
            abort(501, message=str(e))

    @classmethod
    def get_services(cls, services):
        for service in Services.__members__.keys():
            status = systemctl_status(Services[service].value.get('service_file_name'))
            services.append({
                'display_name': Services[service].value.get('display_name'),
                'app_type': OTHERS,
                'installable': False,
                **status
            })
        for subclass in inheritors(InstallableApp):
            dummy_app = subclass()
            status = systemctl_status(dummy_app.service_file_name)
            services.append({
                'display_name': dummy_app.display_name,
                'app_type': dummy_app.app_type,
                'installable': True,
                **status
            })
        return services
