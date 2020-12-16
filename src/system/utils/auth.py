import os


def get_auth_file():
    return os.path.join(os.environ.get("data_dir"), 'auth.txt')
