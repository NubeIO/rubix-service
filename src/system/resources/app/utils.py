from flask_restful import abort

from src import InstallableApp


def get_app_from_service(service, version='') -> InstallableApp:
    try:
        app = InstallableApp.get_app(service, version)
        return app
    except Exception as e:
        abort(404, message=str(e))
