from flask_restful import abort
from packaging import version

from src import InstallableApp


def get_app_from_service(service, version_='') -> InstallableApp:
    try:
        app = InstallableApp.get_app(service, version_)
        if not version_ or version.parse(app.min_support_version()) <= version.parse(version_):
            return app
        abort(400, message='Your version need to be version <= {}'.format(app.min_support_version()))
    except ModuleNotFoundError as e:
        abort(404, message=str(e))
