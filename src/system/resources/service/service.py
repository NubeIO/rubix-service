from flask_restful import Resource, marshal_with, fields

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.service.utils import Services


class ServiceResource(Resource):
    fields = {
        'display_name': fields.String,
        'service': fields.String,
    }

    @classmethod
    @marshal_with(fields)
    def get(cls):
        services = []
        for service in Services.__members__.keys():
            services.append({'display_name': Services[service].value.get('display_name'), 'service': service})
        for subclass in inheritors(InstallableApp):
            services.append({'display_name': subclass().display_name, 'service': subclass.service()})
        return services
