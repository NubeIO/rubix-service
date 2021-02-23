import shutil

from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException, PreConditionException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service, check_wires_plat
from src.system.utils.file import is_dir_exist, delete_existing_folder


class InstallResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        version: str = args['version']
        app: InstallableApp = get_app_from_service(service, version)
        if app.need_wires_plat and not check_wires_plat():
            raise PreConditionException('Please add wires-plat details at first')
        if not is_dir_exist(app.get_downloaded_dir()):
            raise NotFoundException(f'Please download service {service} with version {version} at first')
        backup_data: bool = app.backup_data()
        delete_existing_folder(app.get_installation_dir())
        shutil.copytree(app.get_downloaded_dir(), app.get_installed_dir())
        installation: bool = app.install()
        delete_existing_folder(app.get_download_dir())
        return {'service': service, 'version': version, 'installation': installation, 'backup_data': backup_data}
