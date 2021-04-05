import json
import os

from flask import send_from_directory
from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service, get_installed_app_details
from src.system.resources.fields import config_fields


class ConfigResource(RubixResource):
    @classmethod
    def get(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        filename = 'config.json'
        directory = os.path.join(app.get_global_dir(), 'config')
        if not os.path.exists(f'{directory}/{filename}'):
            raise NotFoundException(f'Service {service.upper()} does not have {filename}')
        return send_from_directory(directory=directory,
                                   filename=filename,
                                   as_attachment=True)

    @classmethod
    @marshal_with(config_fields)
    def put(cls, service):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=dict, required=True)
        args = parser.parse_args()
        data: dict = args['data']
        app: InstallableApp = get_app_from_service(service.upper())
        json_data = json.dumps(data, indent=2)
        update = app.update_config_file(json_data)
        app_details = get_installed_app_details(app) or {}
        return {'service': service.upper(), 'update': update, **app_details}

    @classmethod
    @marshal_with(config_fields)
    def delete(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        delete = app.delete_config_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service.upper(), 'delete': delete, **app_details}


class LoggingResource(RubixResource):
    @classmethod
    def get(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        filename = 'logging.conf'
        directory = os.path.join(app.get_global_dir(), 'config')
        if not os.path.exists(f'{directory}/{filename}'):
            raise NotFoundException(f'Service {service.upper()} does not have {filename}')
        return send_from_directory(directory=directory,
                                   filename=filename,
                                   as_attachment=True)

    @classmethod
    @marshal_with(config_fields)
    def put(cls, service):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        data: str = args['data']
        app: InstallableApp = get_app_from_service(service.upper())
        update = app.update_logging_file(data)
        app_details = get_installed_app_details(app) or {}
        return {'service': service.upper(), 'update': update, **app_details}

    @classmethod
    @marshal_with(config_fields)
    def delete(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        delete = app.delete_logging_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service.upper(), 'delete': delete, **app_details}


class EnvResource(RubixResource):
    @classmethod
    def get(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        filename = '.env'
        directory = os.path.join(app.get_global_dir(), 'config')
        if not os.path.exists(f'{directory}/{filename}'):
            raise NotFoundException(f'Service {service.upper()} does not have {filename}')
        return send_from_directory(directory=directory,
                                   filename=filename,
                                   as_attachment=True)

    @classmethod
    @marshal_with(config_fields)
    def put(cls, service):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        data: str = args['data']
        app: InstallableApp = get_app_from_service(service.upper())
        update = app.update_env_file(data)
        app_details = get_installed_app_details(app) or {}
        return {'service': service.upper(), 'update': update, **app_details}

    @classmethod
    @marshal_with(config_fields)
    def delete(cls, service):
        app: InstallableApp = get_app_from_service(service.upper())
        delete = app.delete_env_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service.upper(), 'delete': delete, **app_details}
