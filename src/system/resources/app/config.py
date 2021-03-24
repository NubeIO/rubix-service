import json

from flask_restful import reqparse, marshal_with
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service, get_installed_app_details
from src.system.resources.fields import config_fields


class UpdateConfigResource(RubixResource):
    @classmethod
    @marshal_with(config_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=dict, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        data: dict = args['data']
        app: InstallableApp = get_app_from_service(service)
        json_data = json.dumps(data, indent=2)
        update = app.update_config_file(json_data)
        if update:
            app.restart()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}


class UpdateLoggingResource(RubixResource):
    @classmethod
    @marshal_with(config_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        data: str = args['data']
        app: InstallableApp = get_app_from_service(service)
        update = app.update_config_file(data)
        if update:
            app.restart()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}


class UpdateEnvResource(RubixResource):
    @classmethod
    @marshal_with(config_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        data: str = args['data']
        app: InstallableApp = get_app_from_service(service)
        update = app.update_env_file(data)
        if update:
            app.restart()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}
