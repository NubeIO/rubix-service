import shutil

from flask import request
from registry.registry import RubixRegistry
from rubix_http.exceptions.exception import PreConditionException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service
from src.system.resources.rest_schema.schema_install import install_attributes
from src.system.utils.data_validation import validate_args
from src.system.utils.file import is_dir_exist, delete_existing_folder


class InstallResource(RubixResource):
    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, install_attributes):
            raise PreConditionException('Invalid request.')
        install_res = []
        args.append(args.pop(next((i for i, item in enumerate(args) if item["service"].upper() == "RUBIX_PLAT"), -1)))
        for arg in args:
            service = arg['service'].upper()
            version = arg['version']
            res = {'service': service, 'version': version, 'installation': False, 'backup_data': False, 'error': ''}
            try:
                app: InstallableApp = get_app_from_service(service, version)
                if app.need_wires_plat and not RubixRegistry().read_wires_plat():
                    res = {**res, 'error': 'Please add wires-plat details at first'}
                if not is_dir_exist(app.get_downloaded_dir()):
                    res = {**res,
                           'error': f'Please download service {app.service()} with version {app.version} at first'}
                if not res.get('error'):
                    backup_data: bool = app.backup_data()
                    delete_existing_folder(app.get_installation_dir())
                    shutil.copytree(app.get_downloaded_dir(), app.get_installed_dir())
                    installation: bool = app.install()
                    delete_existing_folder(app.get_download_dir())
                    res = {**res, 'installation': installation, 'backup_data': backup_data}
            except Exception as e:
                res = {**res, 'error': str(e)}
            install_res.append(res)
        return install_res
