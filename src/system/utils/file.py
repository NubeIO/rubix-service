import os
import shutil
from io import BytesIO
from logging import Logger
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

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


def read_file(file) -> str:
    try:
        with open(file, "r") as f:
            return f.read()
    except Exception:
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


def download_unzip_service(download_link, directory, token, is_asset) -> str:
    import requests

    headers: dict = {}
    if is_asset:
        headers["Accept"] = "application/octet-stream"
    if token:
        headers['Authorization'] = f'Bearer {token}'
    r = requests.get(download_link, headers=headers)
    with ZipFile(BytesIO(r.content)) as z_file:
        z_file.extractall(directory)
    return z_file.namelist()[0]


def upload_unzip_service(file, directory) -> str:
    with ZipFile(file) as z_file:
        z_file.extractall(directory)
    return z_file.namelist()[0]


def directory_zip_service(directory) -> BytesIO:
    zip_file = BytesIO()
    with ZipFile(zip_file, 'w', ZIP_DEFLATED) as z_file:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                z_file.write(file_path, os.path.basename(file_path))
    zip_file.seek(0)
    return zip_file
