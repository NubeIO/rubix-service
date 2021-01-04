from flask_restful import Resource

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.service.utils import Services


class ServiceResource(Resource):
    @classmethod
    def get(cls):
        services = list(Services.__members__.keys())
        for subclass in inheritors(InstallableApp):
            services.append(subclass.id())
        return services
