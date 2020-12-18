import os


def get_auth_file(data_dir: str = None) -> str:
    return os.path.join(data_dir or os.environ.get("data_dir"), 'auth.txt')
