import json
import shutil
from typing import Union, List, Dict

from flask import current_app
from packaging import version
from rubix_http.exceptions.exception import NotFoundException

from src import AppSetting
from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.enums import DownloadState
from src.system.utils.file import get_extracted_dir, write_file, read_file, is_dir_exist, delete_existing_folder
from src.system.utils.shell import systemctl_status


def get_app_from_service(service, version_='') -> InstallableApp:
    try:
        if version_.upper() == 'LATEST':
            app: InstallableApp = InstallableApp.get_app(service, '')
            app_setting = current_app.config[AppSetting.FLASK_KEY]
            app.set_version(app.get_latest_release(app_setting.token))
        else:
            app: InstallableApp = InstallableApp.get_app(service, version_)
        if not version_ or version.parse(app.min_support_version) <= version.parse(app.version):
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
            services = []
            for arg in args:
                _service = arg['service'].upper()
                _version = arg['version']
                service = {'service': _service, 'version': _version, 'download': False, 'error': ''}
                try:
                    app: InstallableApp = get_app_from_service(_service, _version)
                    app.download()
                    services.append({**service, 'version': app.version, 'download': True})
                except (Exception, NotFoundException) as e:
                    services.append({**service, 'download': False, 'error': str(e)})
            update_download_state(DownloadState.DOWNLOADED, services)


def install_app_async(app_context, arg):
    if app_context:
        with app_context():
            return install_app(arg)


def install_app(arg):
    _service = arg['service'].upper()
    _version = arg['version']
    res = {'service': _service, 'version': _version, 'installation': False, 'backup_data': False, 'error': ''}
    try:
        app: InstallableApp = get_app_from_service(_service, _version)
        if not is_dir_exist(app.get_downloaded_dir()):
            res = {
                **res, 'version': app.version,
                'error': f'Please download service {app.service} with version {app.version} at first'
            }
        if not res.get('error'):
            backup_data: bool = app.backup_data()
            delete_existing_folder(app.get_installation_dir())
            shutil.copytree(app.get_downloaded_dir(), app.get_installed_dir())
            installation: bool = app.install()
            delete_existing_folder(app.get_download_dir())
            res = {**res, 'version': app.version, 'installation': installation, 'backup_data': backup_data}
    except (Exception, NotFoundException) as e:
        res = {**res, 'error': str(e)}
    return res


def update_download_state(state: DownloadState, services: List[Dict] = None):
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    write_file(app_setting.download_status_file,
               json.dumps({"state": state.name, "services": services if services else []}))


def get_download_state():
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    return json.loads(read_file(app_setting.download_status_file) or "{}") \
        or {"state": DownloadState.CLEARED.name, "services": []}
