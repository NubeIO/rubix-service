import os
import shutil
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


def delete_existing_folder(dir_):
    dir_path = Path(dir_)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)
        return True
    else:
        return False


def download_unzip_service(url, directory):
    try:
        with urlopen(url) as zip_resp:
            with ZipFile(BytesIO(zip_resp.read())) as z_file:
                z_file.extractall(directory)
                return True
    except FileNotFoundError:
        return False


def get_extracted_dir(home_dir) -> str:
    try:
        dirs = os.listdir(home_dir)
        if len(dirs):
            return os.path.join(home_dir, dirs[0])
    except Exception as e:
        print(e)
    return ""
