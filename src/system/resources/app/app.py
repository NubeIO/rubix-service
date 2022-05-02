import enum
from typing import List, Dict

import gevent
from flask import current_app
from flask_restful import fields, marshal_with, reqparse, inputs
from rubix_http.resource import RubixResource
from werkzeug.local import LocalProxy

from src import AppSetting
from src.inheritors import get_instance
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_installed_app_details, get_app_from_service, get_github_token
from src.system.resources.fields import service_fields
from src.system.resources.service.utils import get_service_restart_job
from src.system.utils.shell import systemctl_installed

logger = LocalProxy(lambda: current_app.logger)


class BackgroundProcessType(enum.Enum):
    APP_STAT = 'AppStat'
    LATEST_VERSION = 'LatestVersion'


class AppResource(RubixResource):
    fields = {
        'version': fields.String,
        'app_type': fields.String,
        'gateway_access': fields.Boolean,
        'min_support_version': fields.String,
        'port': fields.Integer,
        **service_fields,
        'browser_download_url': fields.String,
        'latest_version': fields.String,
        'device_types': fields.List(fields.String)
    }

    @classmethod
    @marshal_with(fields)
    def get(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('browser_download_url', type=inputs.boolean, default=False)
        parser.add_argument('latest_version', type=inputs.boolean, default=False)
        args = parser.parse_args()
        get_browser_download_url: bool = args['browser_download_url']
        get_latest_version: bool = args['latest_version']
        app_settings = current_app.config[AppSetting.FLASK_KEY].installable_app_settings
        return cls.get_installed_apps(app_settings, get_browser_download_url, get_latest_version)

    @classmethod
    def get_installed_apps(cls, app_settings, get_browser_download_url: bool, get_latest_version: bool) -> List[Dict]:
        installed_apps = []
        processes = []
        for app_setting in app_settings:
            instance = get_instance(InstallableApp, app_setting.app_type)
            if instance is not None:
                instance.set_app_settings(app_setting)
                processes.append(
                    gevent.spawn(cls.get_installed_app_stat_async, current_app._get_current_object().app_context,
                                 instance, get_browser_download_url))
                if get_latest_version:
                    processes.append(
                        gevent.spawn(cls.get_latest_app_async, current_app._get_current_object().app_context, instance))
        gevent.joinall(processes)
        latest_versions: dict = {}
        for process in processes:
            output: dict = process.value
            if output.get('type') == BackgroundProcessType.APP_STAT.name:
                installed_apps.append(process.value)
            else:
                latest_versions[output.get('service')] = output.get('latest_version')
        for installed_app in installed_apps:
            installed_app['latest_version'] = latest_versions.get(installed_app.get('service'))
            installed_app['restart_job'] = get_service_restart_job(installed_app.get('service'))
        return installed_apps

    @classmethod
    def get_latest_app_async(cls, app_context, app: InstallableApp) -> dict:
        with app_context():
            return {
                'latest_version': cls.get_latest_app(app),
                'type': BackgroundProcessType.LATEST_VERSION.name,
                'service': app.service
            }

    @classmethod
    def get_latest_app(cls, app: InstallableApp) -> dict:
        latest_version = None
        try:
            latest_version = app.get_latest_release(get_github_token())
        except Exception as e:
            logger.error(str(e))
        return latest_version

    @classmethod
    def get_installed_app_stat_async(cls, app_context, app: InstallableApp, get_browser_download_url: bool) -> dict:
        with app_context():
            return {
                **cls.get_installed_app_stat(app, get_browser_download_url),
                'type': BackgroundProcessType.APP_STAT.name
            }

    @classmethod
    def get_installed_app_stat(cls, app: InstallableApp, get_browser_download_url: bool) -> dict:
        details: dict = {}
        is_installed: bool = False
        _browser_download_url = {}
        if systemctl_installed(app.service_file_name):
            details = get_installed_app_details(app)
            if details:
                is_installed = True
                app: InstallableApp = get_app_from_service(details['service'])
                app.set_version(details['version'])
                if get_browser_download_url:
                    try:
                        _browser_download_url = app.get_download_link(get_github_token(), True)
                    except Exception as e:
                        logger.error(str(e))
        return {
            **(details if details else app.to_property_dict()),
            **_browser_download_url,
            'service': app.service,
            'is_installed': is_installed,
        }


class AppLatestResource(RubixResource):
    @classmethod
    def get(cls):
        app_settings = current_app.config[AppSetting.FLASK_KEY].installable_app_settings
        processes = []
        for app_setting in app_settings:
            app: InstallableApp = get_instance(InstallableApp, app_setting.app_type)
            if app:
                app.set_app_settings(app_setting)
                processes.append(
                    gevent.spawn(AppResource.get_latest_app_async, current_app._get_current_object().app_context, app))
        latest_versions: dict = {}
        gevent.joinall(processes)
        for process in processes:
            latest_versions[process.value.get('service')] = process.value.get('latest_version')
        return latest_versions
