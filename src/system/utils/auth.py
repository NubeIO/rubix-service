import os

from src.envs import DATA_DIR_ENV


def get_auth_file(data_dir: str = None) -> str:
    return os.path.join(data_dir or os.environ.get(DATA_DIR_ENV), 'auth.txt')
