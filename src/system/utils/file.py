import logging
import os
import shutil
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen, Request
from zipfile import ZipFile

logger = logging.getLogger(__name__)


def delete_existing_folder(dir_) -> bool:
    dir_path = Path(dir_)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)
        return True
    return False


def delete_all_folders_except(parent_dir, dir_) -> None:
    """It deletes all folders inside the parent_dir except dir_"""
    dir_path = Path(dir_)
    if dir_path.exists():
        dirs = os.listdir(parent_dir)
        for dir__ in dirs:
            if dir__ != dir_:
                os.remove(os.path.join(parent_dir, dir__))


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


def read_file(file) -> str:
    try:
        f = open(file, "r")
        return f.read()
    except Exception as e:
        logger.error(e)
        return ""


def write_file(file, content):
    f = open(file, "w")
    f.write(content)
    f.close()


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
