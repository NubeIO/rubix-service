from packaging import version
from rubix_http.exceptions.exception import NotFoundException

from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import get_extracted_dir
from src.system.utils.shell import systemctl_status


def get_app_from_service(service, version_=''):
    try:
        app: InstallableApp = InstallableApp.get_app(service, version_)
        if not version_ or version.parse(app.min_support_version) <= version.parse(version_):
            return app
        raise NotFoundException(f'Your version need to be version <= {app.min_support_version}')
    except ModuleNotFoundError as e:
        raise NotFoundException(str(e))


def get_installed_app_details(dummy_app: InstallableApp):
    _version: str = get_extracted_dir(dummy_app.get_installation_dir())
    if _version:
        status = systemctl_status(dummy_app.service_file_name)
        return {
            **dummy_app.to_property_dict(),
            **status,
            'version': _version.split("/")[-1],
            'service': dummy_app.service(),
        }

    return None
