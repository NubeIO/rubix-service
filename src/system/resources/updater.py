import os
import time
from flask_restful import Resource, reqparse, abort
from src.system.services import Services
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from pathlib import Path
import shutil
from src.system.utils.shell_commands import execute_command
from src.system.utils.url_check import service_urls, IsValidURL

path_global = ""


def set_path_global(_dir):
    global path_global
    path_global = _dir.split('/')[0]


def get_path_global():
    return path_global


def delete_existing_folder(_dir):
    dir_path = Path(_dir)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)
        return True
    else:
        return False


def download_unzip_service(service, _dir):
    print(2222)
    print(service, _dir)
    print(2222)
    try:
        with urlopen(service) as zip_resp:
            with ZipFile(BytesIO(zip_resp.read())) as z_file:
                z_file.extractall(_dir)
                dirs = list(set([os.path.dirname(x) for x in z_file.namelist()]))
                set_path_global(dirs[0])
                get_path_global()
                return True
    except FileNotFoundError:
        return False


def build_install_cmd(_dir, user, lib_dir):
    # sudo bash script.bash start -u=<pi|debian> -dir=<bacnet_flask_dir> -lib_dir=<common-py-libs-dir>
    build_dir = "{}/{}".format(_dir, get_path_global())
    print(9999, build_dir, get_path_global())
    cmd = "sudo bash script.bash start -u={} -dir={} -lib_dir={}".format(user, build_dir, lib_dir)
    return [cmd, build_dir]


def build_install_cmd_wires(_dir, user):
    # sudo bash script.bash start -u=<pi|debian> -dir=<bacnet_flask_dir> -lib_dir=<common-py-libs-dir>
    build_dir = "{}/{}".format(_dir, get_path_global())
    wires_path = 'rubix-wires'

    "bash script.bash start -u=pi -hp=/home/pi -l=false"
    cmd = "bash script.bash start -u={} -hp={}/{} -l=false".format(user, build_dir, wires_path)
    print(9999, build_dir, get_path_global())
    print(9999, cmd)
    return [cmd, build_dir]


def build_install(cmd, test, cwd):
    if test:
        time.sleep(5)
        return True
    run = execute_command(cmd, cwd)
    if not run:
        return False
    else:
        return True


def _validate_service(service) -> str:
    if service.upper() in Services.__members__.keys():
        return service_urls.get(service)
    else:
        abort(400, message="service {} does not exist in our system".format(service))


class DownloadService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('build_url', type=str, required=True)
        parser.add_argument('directory', type=str, required=True)
        args = parser.parse_args()
        _service = args['service']
        build_url = args['build_url']
        directory = args['directory']
        service = _validate_service(_service)
        if not service:
            abort(400, message="service {} does not exist in our system".format(service))
        url = IsValidURL(build_url, _service)
        service_url = url.service_to_url()
        check_url = url.check_url(service_url)
        print(11111, url, service_url, check_url)
        if not check_url:
            abort(400, message="service {} is an invalid url".format(service))
        print(">>>>>>> delete_existing_dir")
        delete_existing_dir = delete_existing_folder(directory)
        print(">>>>>>> download")
        download = download_unzip_service(build_url, directory)
        if not download:
            abort(400, message="valid URL service {} but download failed check internet!".format(service))
        return {'service': service, 'service_to_url': service_url, 'del_existing_dir': delete_existing_dir}


class InstallService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('_dir', type=str, required=True)
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('lib_dir', type=str, required=False)
        parser.add_argument('test_install', type=bool, required=True)
        args = parser.parse_args()
        _service = args['service']
        _dir = args['_dir']
        user = args['user']
        lib_dir = args['lib_dir']
        test_install = args['test_install']
        service = _validate_service(_service)
        print(">>>>>>> INSTALL")
        print(_dir, user, lib_dir, _service)

        if not service:
            abort(400, message="service {} does not exist in our system".format(service))
        if _service == "WIRES":
            print(">>>>>>> INSTALL WIRES")
            build_cmd = build_install_cmd_wires(_dir, user)
            print(_service, build_cmd, test_install)
            install = build_install(build_cmd[0], test_install, build_cmd[1])
            if not install:
                abort(400, message="valid service {} issue on install, build cmd: {}".format(service, build_cmd))
            return {'service': service, 'build_cmd': build_cmd, 'install_completed': install}
        elif _service == "BAC_REST" or _service == "BAC_SERVER":
            print(">>>>>>> INSTALL BAC_REST OR BAC_SERVER")
            build_cmd = build_install_cmd(_dir, user, lib_dir)
            print(_service, build_cmd, test_install)
            install = build_install(build_cmd[0], test_install, build_cmd[1])
            if not install:
                abort(400, message="valid service {} issue on install, build cmd: {}".format(service, build_cmd))
            return {'service': service, 'build_cmd': build_cmd, 'install_completed': install}
