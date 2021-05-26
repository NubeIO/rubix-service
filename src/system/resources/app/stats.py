from flask import current_app
from flask_restful import marshal_with, reqparse, inputs
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src import AppSetting
from src.system.resources.app.app import AppResource


class AppStatsResource(RubixResource):
    @classmethod
    @marshal_with(AppResource.fields)
    def get(cls, service):
        parser = reqparse.RequestParser()
        parser.add_argument('browser_download_url', type=inputs.boolean, default=False)
        parser.add_argument('latest_version', type=inputs.boolean, default=False)
        args = parser.parse_args()
        get_browser_download_url = args['browser_download_url']
        get_latest_version = args['latest_version']
        app_settings = current_app.config[AppSetting.FLASK_KEY].installable_app_settings
        app_settings_params = []
        for app_setting in app_settings:
            if app_setting.service == service:
                app_settings_params = [app_setting]
                break
        if app_settings_params:
            return AppResource.get_installed_apps(app_settings_params, get_browser_download_url, get_latest_version)[0]
        else:
            raise NotFoundException(f'Not found service {service}')
