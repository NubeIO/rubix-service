from flask_restful import Resource, abort

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.shell import systemctl_status


class AppResource(Resource):
    @classmethod
    def get(cls):
        try:
            apps = []
            for subclass in inheritors(InstallableApp):
                dummy_app: InstallableApp = subclass()
                app: dict = dummy_app.to_property_dict()
                app['service'] = dummy_app.service()
                status: dict = systemctl_status(dummy_app.service_file_name)
                apps.append({**app, **status})
            return apps
        except Exception as e:
            abort(501, message=str(e))
