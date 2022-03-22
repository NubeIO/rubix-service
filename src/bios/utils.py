import os

from src.system.utils.file import write_file

BIOS_APP_STATE_FILE_PATH = '/data/rubix-bios/data/app_state.txt'


def clear_bios_app_state() -> bool:
    if not os.path.exists(BIOS_APP_STATE_FILE_PATH):
        return False
    write_file(BIOS_APP_STATE_FILE_PATH, '')
    return True
