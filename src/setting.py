import json
import os
import secrets
from typing import List

from flask import Flask
from mrb.setting import MqttSetting as MqttRestBridgeSetting
from rubix_mqtt.setting import BaseSetting

from src.pyinstaller import resource_path
from src.system.utils.file import write_file, read_file


class InstallableAppSetting(BaseSetting):
    KEY = 'installable_apps'

    def __init__(self):
        self.app_type = ''
        self.service = ''
        self.display_name = ''
        self.repo_name = ''
        self.service_file_name = ''
        self.data_dir_name = ''
        self.port = 8080
        self.min_support_version = ''
        self.description = "",
        self.gateway_access = False
        self.url_prefix = ''
        self.need_wires_plat = True
        self.pre_start_sleep = 0
        self.working_dir_name = ''
        self.current_working_dir_name = ''
        self.name_contains = ''
        self.systemd_static_wd_value = ''
        self.systemd_file_dir = ''


class AppSetting:
    PORT = 1616
    ROOT_DIR_ENV = 'ROOT_DIR'
    GLOBAL_DIR_ENV = 'GLOBAL_DIR'
    DATA_DIR_ENV = 'RUBIX_SERVICE_DATA'
    CONFIG_DIR_ENV = 'RUBIX_SERVICE_CONFIG'
    ARTIFACT_DIR_ENV = 'ARTIFACT_DIR'
    BACKUP_DATA_DIR_ENV = 'BACKUP_DATA'
    FLASK_KEY: str = 'APP_SETTING'

    default_root_dir: str = 'out'
    default_global_dir: str = 'out/rubix-service'
    default_data_dir: str = 'data'
    default_config_dir: str = 'config'
    default_identifier: str = 'rs'
    default_artifact_dir: str = 'apps'
    default_backup_dir: str = 'backup'
    default_secret_key_file = 'secret_key.txt'
    default_token_file = 'token.txt'
    default_setting_file: str = 'config.json'
    default_logging_conf: str = 'logging.conf'
    default_app_settings_file: str = 'app.json'
    fallback_logging_conf: str = 'config/logging.example.conf'
    fallback_prod_logging_conf: str = 'config/logging.prod.example.conf'
    fallback_app_settings_file = 'config/app.example.json'
    default_users_file = 'users.txt'
    default_slaves_file = 'slaves.json'

    def __init__(self, **kwargs):
        self.__port = kwargs.get('port') or AppSetting.PORT
        self.__root_dir = self.__compute_dir(kwargs.get('root_dir'), self.default_root_dir)
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), self.default_global_dir)
        self.__data_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('data_dir')),
                                             self.__join_global_dir(self.default_data_dir))
        self.__config_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('config_dir')),
                                               self.__join_global_dir(self.default_config_dir))
        self.__artifact_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('artifact_dir')),
                                                 self.__join_global_dir(self.default_artifact_dir))
        self.__backup_dir = self.__compute_dir(self.__join_root_dir(kwargs.get('backup_dir')),
                                               self.__join_root_dir(self.default_backup_dir))
        self.__download_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'download'))
        self.__install_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'install'))
        self.__token_file = os.path.join(self.__data_dir, self.default_token_file)
        self.__identifier = kwargs.get('identifier') or AppSetting.default_identifier
        self.__prod = kwargs.get('prod') or False
        self.__device_type = kwargs.get('device_type')
        self.__secret_key = ''
        self.__secret_key_file = os.path.join(self.__config_dir, self.default_secret_key_file)
        self.__users_file = os.path.join(self.__data_dir, self.default_users_file)
        self.__auth = kwargs.get('auth') or False
        self.__mqtt_rest_bridge_setting: MqttRestBridgeSetting = MqttRestBridgeSetting()
        self.__installable_app_settings: List[InstallableAppSetting] = [InstallableAppSetting()]

    @property
    def port(self):
        return self.__port

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def config_dir(self):
        return self.__config_dir

    @property
    def artifact_dir(self) -> str:
        return self.__artifact_dir

    @property
    def backup_dir(self):
        return self.__backup_dir

    @property
    def download_dir(self) -> str:
        return self.__download_dir

    @property
    def install_dir(self) -> str:
        return self.__install_dir

    @property
    def token(self) -> str:
        return read_file(os.path.join(self.data_dir, self.default_token_file))

    @property
    def identifier(self):
        return self.__identifier

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def device_type(self) -> bool:
        return self.__device_type

    @property
    def secret_key(self) -> str:
        return self.__secret_key

    @property
    def auth(self) -> bool:
        return self.__auth

    @property
    def users_file(self) -> str:
        return self.__users_file

    @property
    def mqtt_rest_bridge_setting(self) -> MqttRestBridgeSetting:
        return self.__mqtt_rest_bridge_setting

    @property
    def installable_app_settings(self) -> List[InstallableAppSetting]:
        return self.__installable_app_settings

    def reload(self, is_json_str: bool = False):
        data = self.__read_file(self.default_setting_file, self.__config_dir, is_json_str)
        self.__mqtt_rest_bridge_setting = self.__mqtt_rest_bridge_setting.reload(data.get('mqtt_rest_bridge_listener'))
        self.__reload_app_settings()
        return self

    def reload_mrb_listener(self, mqtt_rest_bridge_listener):
        data = self.__read_file(self.default_setting_file, self.__config_dir, False)
        self.__mqtt_rest_bridge_setting = self.__mqtt_rest_bridge_setting.reload(mqtt_rest_bridge_listener)
        data = {**data, 'mqtt_rest_bridge_listener': mqtt_rest_bridge_listener}
        write_file(os.path.join(self.__config_dir, self.default_setting_file), json.dumps(data, indent=2))
        return mqtt_rest_bridge_listener

    def init_app(self, app: Flask):
        self.__secret_key = AppSetting.__handle_secret_key(self.__secret_key_file)
        app.config[AppSetting.FLASK_KEY] = self
        return self

    def __join_root_dir(self, _dir):
        return _dir if _dir is None or _dir.strip() == '' else os.path.join(self.__root_dir, _dir)

    def __join_global_dir(self, _dir):
        return _dir if _dir is None or _dir.strip() == '' else os.path.join(self.__global_dir, _dir)

    def __reload_app_settings(self):
        app_setting = os.path.join(self.__config_dir, self.default_app_settings_file)
        if not os.path.isfile(app_setting):
            app_setting = resource_path(self.fallback_app_settings_file)
        data = self.__read_file(app_setting, "", False)
        installable_app_settings = data.get(InstallableAppSetting.KEY, [])
        if len(installable_app_settings) > 0:
            self.__installable_app_settings = [InstallableAppSetting().reload(s) for s in installable_app_settings]

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __handle_secret_key(secret_key_file) -> str:
        if AppSetting.auth:
            existing_secret_key = read_file(secret_key_file)
            if existing_secret_key.strip():
                return existing_secret_key

            secret_key = AppSetting.__create_secret_key()
            write_file(secret_key_file, secret_key)
            return secret_key
        return ''

    @staticmethod
    def __create_secret_key():
        return secrets.token_hex(24)

    @staticmethod
    def __read_file(setting_file: str, _dir: str, is_json_str=False):
        if is_json_str:
            return json.loads(setting_file)
        if setting_file is None or setting_file.strip() == '':
            return {}
        s = setting_file if os.path.isabs(setting_file) else os.path.join(_dir, setting_file)
        if not os.path.isfile(s) or not os.path.exists(s):
            return {}
        with open(s) as json_file:
            return json.load(json_file)
