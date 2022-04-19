import json
import os
import shutil
from abc import ABC

import requests
from flask import current_app
from werkzeug.local import LocalProxy

from src import AppSetting
from src.pyinstaller import resource_path
from src.system.apps.base.systemd_app import SystemdApp
from src.system.apps.enums.enums import Types
from src.system.utils.file import download_unzip_service, delete_file, delete_existing_folder

logger = LocalProxy(lambda: current_app.logger)


def select_plugin_download_link(plugin: str, row: any):
    setting = current_app.config[AppSetting.FLASK_KEY]
    for asset in row.get('assets', []):
        artifact_name: str = asset.get('name')
        if setting.device_type in artifact_name and plugin in artifact_name:
            return asset.get('url')


def get_plugin_file_name(plugin: str):
    setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    return f'{plugin}-{setting.device_type}.so'


class GoFFApp(SystemdApp, ABC):
    def __init__(self):
        super().__init__()

    @property
    def app_type(self):
        return Types.GO_FF_APP.value

    @property
    def select_in(self) -> bool:
        return True

    @property
    def select_in_content(self) -> str:
        return "flow-framework"

    # noinspection DuplicatedCode
    def create_service(self):
        lines = []
        with open(resource_path('systemd/nubeio-app-ff-go-app-service.service')) as systemd_file:
            wd: str = self.get_wd()
            global_dir: str = self.get_global_dir()
            for line in systemd_file.readlines():
                if '<pre_start_sleep>' in line:
                    line = line.replace('<pre_start_sleep>', str(self.pre_start_sleep))
                if '<working_dir>' in line and wd:
                    line = line.replace('<working_dir>', wd)
                if '<port>' in line and self.port:
                    line = line.replace('<port>', str(self.port))
                if '<global_dir>' in line and global_dir:
                    line = line.replace('<global_dir>', global_dir)
                if '<name>' in line and self.repo_name:
                    line = line.replace('<name>', self.repo_name)
                if '<description>' in line and self.description:
                    line = line.replace('<description>', self.description)
                lines.append(line)
        return lines

    def get_plugin_list(self, token: str):
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        release_link: str = f'https://api.github.com/repos/NubeIO/{self.repo_name}/releases/tags/{self.version}'
        resp = requests.get(release_link, headers=headers)
        row: any = json.loads(resp.content)
        return self._select_plugin_list(row)

    def download_plugins(self, plugins: list) -> list:
        download_res = []
        delete_existing_folder(self.get_plugin_download_dir())
        from src.system.resources.app.utils import get_github_token
        token: str = get_github_token()
        plugin_download_links = self._get_plugin_download_links(token, plugins)
        for plugin_download_link in plugin_download_links:
            plugin: str = plugin_download_link['plugin']
            download_link: str = plugin_download_link['download_link']
            error = plugin_download_link['error']
            if error:
                download_res.append({'plugin': plugin, 'download': False, 'error': error})
            else:
                try:
                    download_unzip_service(download_link, self.get_plugin_download_dir(), token,
                                           self.is_asset)
                    download_res.append({'plugin': plugin, 'download': True, 'error': ""})
                except Exception as e:
                    download_res.append({'plugin': plugin, 'download': False, 'error': str(e)})
        return download_res

    def download_installed_plugin(self):
        installed_path: str = self.get_plugin_installation_dir()
        if os.path.exists(installed_path):
            plugins = [x.split('-')[0] for x in os.listdir(installed_path)]
            self.download_plugins(plugins)

    def install_plugin(self, plugin) -> bool:
        try:
            mode = 0o744
            plugin_file_name = get_plugin_file_name(plugin)
            plugin_download_file = os.path.join(self.get_plugin_download_dir(), plugin_file_name)
            if os.path.exists(plugin_download_file):
                plugin_installation_dir: str = self.get_plugin_installation_dir()
                plugin_installation_file: str = os.path.join(plugin_installation_dir, plugin_file_name)
                os.makedirs(plugin_installation_dir, mode, True)
                shutil.copy(plugin_download_file, plugin_installation_file)
                delete_file(plugin_download_file)
                return True
        except Exception as e:
            logger.info(str(e))
        return False

    def install_plugins(self) -> bool:
        try:
            plugin_installation_dir = self.get_plugin_installation_dir()
            delete_existing_folder(plugin_installation_dir)
            plugin_download_dir: str = self.get_plugin_download_dir()
            if not os.path.exists(plugin_download_dir):
                return False
            shutil.copytree(plugin_download_dir, plugin_installation_dir)
            delete_existing_folder(plugin_download_dir)
        except Exception as e:
            logger.info(str(e))
            return False
        return True

    def uninstall_plugin(self, plugin) -> bool:
        try:
            plugin_file_name = get_plugin_file_name(plugin)
            file = os.path.join(self.get_plugin_installation_dir(), plugin_file_name)
            delete_file(file)
        except Exception as e:
            logger.info(str(e))
            return False
        return True

    def _get_plugin_download_links(self, token: str, plugins: list):
        download_links = []
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        release_link: str = f'https://api.github.com/repos/NubeIO/{self.repo_name}/releases/tags/{self.version}'
        resp = requests.get(release_link, headers=headers)
        row: any = json.loads(resp.content)
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        for plugin in plugins:
            download_link = select_plugin_download_link(plugin, row)
            if not download_link:
                error: str = f'No plugin {plugin} for type {setting.device_type} & version {self.version}, ' \
                             f'check your token & repo'
                download_links.append({'plugin': plugin, 'download_link': download_link, 'error': error})
            download_links.append({'plugin': plugin, 'download_link': download_link, 'error': ''})
        return download_links

    def _select_plugin_list(self, row: any):
        setting = current_app.config[AppSetting.FLASK_KEY]
        plugins: list = []
        for asset in row.get('assets', []):
            artifact_name: str = asset.get('name')
            if setting.device_type in artifact_name and (self.select_in_content not in artifact_name):
                plugin = asset.get('name').split(f"-{row.get('tag_name')[1:]}", 1)[0]
                plugin_file_name = get_plugin_file_name(plugin)
                plugins.append({
                    'version': row.get('tag_name'),
                    'name': plugin,
                    'is_installed': os.path.exists(os.path.join(self.get_plugin_installation_dir(),
                                                                plugin_file_name)),
                    'created_at': row.get('created_at')
                })
        return plugins
