import os

from flask_restful import Resource, reqparse, abort

from src.system.services import validate_installation_service, InstallableServices, installation_dir
from src.system.utils.file import delete_existing_folder, download_unzip_service, get_extracted_dir
from src.system.utils.shell_commands import execute_command
from src.system.utils.url_check import ServiceURL


class DownloadService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('build_url', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        build_url = args['build_url']
        does_service_exist = validate_installation_service(service)
        if not does_service_exist:
            abort(404, message=f"service {service} does not exist in our system")
        os.makedirs(installation_dir[service], 0o775, exist_ok=True)  # create dir if doesn't exist
        service_url = ServiceURL(build_url, service)
        if not service_url.is_valid():
            abort(400, message=f"service {service} is an invalid build_url")
        delete_existing_dir = delete_existing_folder(installation_dir[service])
        download = download_unzip_service(build_url, installation_dir[service])
        if not download:
            abort(501, message=f"valid URL service {service} but download failed check internet or version!")
        return {'service': service, 'build_url': build_url, 'del_existing_dir': delete_existing_dir}


class InstallService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        user = args['user']
        lib_dir = args['lib_dir']

        cwd = _validate_installation_service_and_get_cmd(service)
        if service == InstallableServices.WIRES.name:
            wd = _get_wd_wires(installation_dir[service])
            cmd = _get_install_cmd_wires(user, wd)
        else:
            cmd = _get_install_cmd_apps(user, cwd, lib_dir)

        install = execute_command(cmd, cwd)
        if not install:
            abort(400, message=f"valid service {service} issue on install, build cmd: {cmd} on working dir: {cwd}")
        return {'service': service, 'cmd': cmd, cwd: 'cwd', 'install completed': install}


class DeleteDataBaseDir(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()

        cwd = _validate_installation_service_and_get_cmd(service)
        cmd = _get_delete_data_cmd()
        delete_data = execute_command(cmd, cwd)
        if not delete_data:
            abort(400, message=f"valid service {service} issue on delete_data, build cmd: {cmd} on working dir: {cwd}")
        return {'service': service, 'cmd': cmd, cwd: 'cwd', 'delete_data completed': delete_data}


class DeleteInstallationDir(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()

        cwd = _validate_installation_service_and_get_cmd(service)
        cmd = _get_delete_cmd()
        delete = execute_command(cmd, cwd)
        if not delete:
            abort(400,
                  message=f"valid service {service} issue on delete, build cmd: {cmd} on working dir: {cwd}")
        app_dir_delete = delete_existing_folder(installation_dir[service])
        return {'service': service, 'cmd': cmd, cwd: 'cwd', 'app_dir_delete': app_dir_delete}


def _validate_installation_service_and_get_cmd(service):
    does_service_exist = validate_installation_service(service)
    if not does_service_exist:
        abort(400, message=f"service {service} does not exist in our system")
    if service == InstallableServices.WIRES.name:
        cwd = _get_cwd_wires(installation_dir[service])
    else:
        cwd = _get_cwd_apps(installation_dir[service])
    return cwd


def _get_cwd_apps(dir_) -> str:
    cwd = get_extracted_dir(dir_)
    if not cwd:
        abort(f"Check {dir_}, we don't have any files inside this dir")
    return cwd


def _get_cwd_wires(dir_) -> str:
    """current working dir for script.bash execution"""
    cwd = os.path.join(_get_cwd_apps(dir_), 'rubix-wires/systemd')
    return cwd


def _get_wd_wires(dir_) -> str:
    """working dir for systemd"""
    wd = os.path.join(_get_cwd_apps(dir_), 'rubix-wires')
    return wd


def _get_install_cmd_apps(user, wd, lib_dir) -> str:
    """py-apps: sudo bash script.bash start -u=pi -dir=/home/pi/point-server -lib_dir=/home/pi/common-py-libs"""
    cmd = f"sudo bash script.bash start -u={user} -dir={wd} -lib_dir={lib_dir}"
    return cmd


def _get_install_cmd_wires(user, wd) -> str:
    """wires: bash script.bash start -u=pi -dir=/home/pi/wires-build/rubix-wires"""
    cmd = f"sudo bash script.bash start -u={user} -dir={wd}"
    return cmd


def _get_delete_data_cmd() -> str:
    cmd = f"sudo bash script.bash delete_data"
    return cmd


def _get_delete_cmd() -> str:
    cmd = "sudo bash script.bash delete"
    return cmd
