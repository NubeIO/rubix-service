import os

from flask_restful import Resource, reqparse, abort

from src.system.services import validate_installation_service, InstallableServices
from src.system.utils.file import delete_existing_folder, download_unzip_service, get_extracted_dir
from src.system.utils.shell_commands import execute_command
from src.system.utils.url_check import ServiceURL


class DownloadService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('build_url', type=str, required=True)
        parser.add_argument('dir', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        build_url = args['build_url']
        dir_ = args['dir']
        does_service_exist = validate_installation_service(service)
        if not does_service_exist:
            abort(404, message=f"service {service} does not exist in our system")
        service_url = ServiceURL(build_url, service)
        if not service_url.is_valid():
            abort(400, message=f"service {service} is an invalid build_url")
        delete_existing_dir = delete_existing_folder(dir_)
        download = download_unzip_service(build_url, dir_)
        if not download:
            abort(501, message=f"valid URL service {service} but download failed check internet or version!")
        return {'service': service, 'build_url': build_url, 'dir': dir_, 'del_existing_dir': delete_existing_dir}


class InstallService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('dir', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        dir_ = args['dir']
        user = args['user']
        lib_dir = args['lib_dir']
        does_service_exist = validate_installation_service(service)
        if not does_service_exist:
            abort(400, message=f"service {service} does not exist in our system")
        if service == InstallableServices.WIRES.name:
            wd_and_cwd = _get_wd_and_cwd_wires(dir_)
            cwd = wd_and_cwd['cwd']
            cmd = _get_install_cmd_wires(user, wd_and_cwd['wd'])
        else:
            cwd = _get_cwd_apps(dir_)
            cmd = _get_install_cmd_apps(user, cwd, lib_dir)

        install = execute_command(cmd, cwd)
        if not install:
            abort(400, message=f"valid service {service} issue on install, build cmd: {cmd} on working dir: {cwd}")
        return {'service': service, 'cmd': cmd, cwd: 'cwd', 'install completed': install}


class DeleteDataBaseDir(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('dir', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        dir_ = args['dir']
        user = args['user']
        does_service_exist = validate_installation_service(service)
        if not does_service_exist:
            abort(400, message=f"service {service} does not exist in our system")
        if service == InstallableServices.WIRES.name:
            wd_and_cwd = _get_wd_and_cwd_wires(dir_)
            cwd = wd_and_cwd['cwd']
            cmd = _get_uninstall_cmd_wires_installation_dir(wd_and_cwd['wd'])
            cmd_lib_dir = _get_uninstall_cmd_wires_lib_dir()
        else:
            cwd = _get_cwd_apps(dir_)
            cmd = _get_uninstall_cmd_apps_installation_dir(cwd)
            cmd_lib_dir = _get_uninstall_cmd_apps_lib_dir(lib_dir)
        # uninstall = execute_command(cmd, cwd)
        print(22222, cmd, cwd, cmd_lib_dir)
        uninstall = True
        if not uninstall:
            abort(400,
                  message=f"valid service {service} issue on uninstall/remove, build cmd: {cmd} on working dir: {cwd}")
        return {'service': service, 'cmd': cmd, cwd: 'cwd', 'uninstall completed': uninstall}


class DeleteInstallationDir(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('dir', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        args = parser.parse_args()
        service = args['service'].upper()
        dir_ = args['dir']
        user = args['user']
        lib_dir = args['lib_dir']
        does_service_exist = validate_installation_service(service)
        if not does_service_exist:
            abort(400, message=f"service {service} does not exist in our system")
        if service == InstallableServices.WIRES.name:
            wd_and_cwd = _get_wd_and_cwd_wires(dir_)
            cwd = wd_and_cwd['cwd']
            cmd = _get_uninstall_cmd_wires_installation_dir(wd_and_cwd['wd'])
            cmd_lib_dir = _get_uninstall_cmd_wires_lib_dir()
        else:
            cwd = _get_cwd_apps(dir_)
            cmd = _get_uninstall_cmd_apps_installation_dir(cwd)
            cmd_lib_dir = _get_uninstall_cmd_apps_lib_dir(lib_dir)
        # uninstall = execute_command(cmd, cwd)
        print(22222, cmd, cwd, cmd_lib_dir)
        uninstall = True
        if not uninstall:
            abort(400,
                  message=f"valid service {service} issue on uninstall/remove, build cmd: {cmd} on working dir: {cwd}")
        return {'service': service, 'cmd': cmd, cwd: 'cwd', 'uninstall completed': uninstall}


def _get_cwd_apps(dir_) -> str:
    cwd = get_extracted_dir(dir_)
    if not cwd:
        abort(f"Check {dir_}, we don't have any files inside this dir")
    return cwd


def _get_wd_and_cwd_wires(dir_) -> dict:
    return {
        'wd': os.path.join(_get_cwd_apps(dir_), 'rubix-wires'),  # working dir for systemd
        'cwd': os.path.join(_get_cwd_apps(dir_), 'rubix-wires/systemd')  # current working dir for script.bash execution
    }


# py-apps sudo bash script.bash start -u=pi -dir=/home/pi/point-server -lib_dir=/home/pi/common-py-libs

def _get_install_cmd_apps(user, wd, lib_dir) -> str:
    cmd = f"sudo bash script.bash start -u={user} -dir={wd} -lib_dir={lib_dir}"
    return cmd


# wires bash script.bash start -u=pi -hp=/home/pi -l=false
def _get_install_cmd_wires(user, wd) -> str:
    cmd = f"sudo bash script.bash start -u={user} -dir={wd} -l=false"
    return cmd


def _get_uninstall_cmd_apps_database_dir(lib_dir) -> str:
    cmd = f"sudo rm -r {lib_dir}"
    print(cmd, '_get_uninstall_cmd_apps_lib_dir')
    return cmd


def _get_uninstall_cmd_apps_installation_dir(wd) -> str:
    cmd = f"sudo rm -r {wd} "
    print(cmd, '_get_uninstall_cmd_apps_installation_dir')
    return cmd


def _get_uninstall_cmd_wires_installation_dir(wd) -> str:
    cmd = f"sudo rm -r {wd}/wires-builds"
    print(cmd, '_get_uninstall_cmd_wires_installation_dir')
    return cmd


def _get_uninstall_cmd_wires_lib_dir() -> str:
    cmd = f"sudo rm -r /data/rubix-wries"
    print(cmd, '_get_uninstall_cmd_wires_lib_dir')
    return cmd
