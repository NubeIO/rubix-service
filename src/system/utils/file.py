import logging
import os
import shutil
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen, Request
from zipfile import ZipFile

logger = logging.getLogger(__name__)


def delete_existing_folder(dir_):
    dir_path = Path(dir_)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)
        return True
    else:
        return False


def download_unzip_service(url, directory, token):
    try:
        req = Request(url)
        if token:
            req.add_header("Authorization", "token {}".format(token))
        with urlopen(req) as zip_resp:
            with ZipFile(BytesIO(zip_resp.read())) as z_file:
                z_file.extractall(directory)
                return True
    except FileNotFoundError:
        return False


def get_extracted_dir(parent_dir) -> str:
    try:
        dirs = os.listdir(parent_dir)
        if len(dirs):
            return os.path.join(parent_dir, dirs[0])
    except Exception as e:
        logger.error(e)
    return ""


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
