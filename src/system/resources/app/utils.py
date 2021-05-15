import json
from typing import Union

from flask import current_app
from packaging import version
from rubix_http.exceptions.exception import NotFoundException

from src import AppSetting
from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import get_extracted_dir, write_file, read_file
from src.system.utils.shell import systemctl_status


def get_app_from_service(service, version_='') -> InstallableApp:
    try:
        app: InstallableApp = InstallableApp.get_app(service, version_)
        if not version_ or version.parse(app.min_support_version) <= version.parse(version_):
            return app
        raise NotFoundException(f'Your version need to be version >= {app.min_support_version}')
    except ModuleNotFoundError as e:
        raise NotFoundException(str(e))


def get_installed_app_details(dummy_app: InstallableApp) -> Union[dict, None]:
    _version: str = get_extracted_dir(dummy_app.get_installation_dir())
    if _version:
        status = systemctl_status(dummy_app.service_file_name)
        return {
            **dummy_app.to_property_dict(),
            **status,
            'version': _version.split("/")[-1],
            'service': dummy_app.service,
        }

    return None


def download_async(app_context, args):
    if app_context:
        with app_context():
            stat = {"downloading": True, "services": []}
            update_download_state(stat)
            services = []
            for arg in args:
                _service = arg['service'].upper()
                _version = arg['version']
                service = {'service': _service, 'version': _version, 'download': False, 'error': ''}
                try:
                    app: InstallableApp = get_app_from_service(_service, _version)
                    app.download()
                    services.append({**service, 'download': True})
                except (Exception, NotFoundException) as e:
                    services.append({**service, 'download': False, 'error': str(e)})
            stat.update({"downloading": False, "services": services})
            update_download_state(stat)


def update_download_state(stat: dict):
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    write_file(app_setting.download_status_file, json.dumps(stat))


def get_download_state():
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    return json.loads(read_file(app_setting.download_status_file) or "{}")
