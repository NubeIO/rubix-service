import json

from flask_restful import reqparse, marshal_with
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service, get_installed_app_details
from src.system.resources.fields import config_fields


class ConfigResource(RubixResource):
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
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}

    @classmethod
    @marshal_with(config_fields)
    def delete(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete = app.delete_config_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'delete': delete, **app_details}


class LoggingResource(RubixResource):
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
        update = app.update_logging_file(data)
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}

    @classmethod
    @marshal_with(config_fields)
    def delete(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete = app.delete_logging_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'delete': delete, **app_details}


class EnvResource(RubixResource):
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
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}

    @classmethod
    @marshal_with(config_fields)
    def delete(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service: str = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete = app.delete_env_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'delete': delete, **app_details}

