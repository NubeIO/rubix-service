from src.system.utils.file import write_file

BIOS_APP_STATE_FILE_PATH = '/data/rubix-bios/data/app_state.txt'


def clear_bios_app_state():
    write_file(BIOS_APP_STATE_FILE_PATH, '')
