from src import AppSetting
from src.system.utils.file import write_file, read_file, is_file_exist
from src.users.model_users import UserModel


def create_internal_token(app_setting: AppSetting):
    internal_token = UserModel.encode_jwt_token("internal_user").get("access_token")
    if not is_file_exist(app_setting.internal_token_file):
        write_file(app_setting.internal_token_file, internal_token)
        app_setting.internal_token = f'Internal {internal_token}'


def get_internal_token(app_setting: AppSetting) -> str:
    return read_file(app_setting.internal_token_file)
