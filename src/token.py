from src import AppSetting
from src.system.utils.file import write_file
from src.users.model_users import UserModel


def create_internal_token(app_setting: AppSetting):
    if app_setting.auth:
        internal_token = UserModel.encode_jwt_token("internal_user").get("access_token")
        write_file(app_setting.internal_token_file, internal_token)
        app_setting.internal_token = internal_token
