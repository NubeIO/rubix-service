import os
import shutil
from io import BytesIO
from logging import Logger
from pathlib import Path
from urllib.request import urlopen, Request
from zipfile import ZipFile

from flask import current_app
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger) or Logger(__name__)


def delete_existing_folder(dir_) -> bool:
    dir_path = Path(dir_)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_)
        return True
    return False


def is_dir_exist(dir_) -> bool:
    dir_path = Path(dir_)
    return dir_path.exists()


def download_unzip_service(download_link, directory, token) -> str:
    req = Request(download_link)
    if token:
        req.add_header("Authorization", "token {}".format(token))
    with urlopen(req) as zip_resp:
        with ZipFile(BytesIO(zip_resp.read())) as z_file:
            z_file.extractall(directory)
            return z_file.namelist()[0]


def read_file(file, debug=False) -> str:
    try:
        with open(file, "r") as f:
            return f.read()
    except Exception as e:
        if not debug:
            logger.error(e)
        return ""


def write_file(file, content):
    f = open(file, "w")
    f.write(content)
    f.close()


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def get_extracted_dir(parent_dir) -> str:
    dir_path = Path(parent_dir)
    if dir_path.exists():
        dirs = os.listdir(parent_dir)
        if len(dirs):
            return os.path.join(parent_dir, dirs[0])
    return ""
