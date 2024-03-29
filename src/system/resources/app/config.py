import json
import os

from flask import request
from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.enums import Types
from src.system.resources.app.utils import get_app_from_service, get_installed_app_details
from src.system.resources.fields import config_fields, config_delete_fields
from src.system.utils.file import read_file


class ConfigResource(RubixResource):
    @classmethod
    def is_json(cls):
        return True

    @classmethod
    def filename(cls):
        return 'config.json'

    @classmethod
    def directory(cls):
        return 'config'

    @classmethod
    def relative_path(cls):
        return os.path.join(cls.directory(), cls.filename())

    @classmethod
    def get(cls):
        service: str = request.args.get('service')
        if not service:
            raise BadDataException("Include ?service as an argument")
        app: InstallableApp = get_app_from_service(service)
        if app.app_type == Types.APT_APP.value:
            return {"data": read_file(app.app_setting.config_file)}
        else:
            filename = cls.filename()
            directory = os.path.join(app.get_global_dir(), cls.directory())
            file = os.path.join(directory, filename)
            if not os.path.exists(file):
                raise NotFoundException(f'Service {service} does not have {filename}')
            if cls.is_json():
                return {"data": json.loads(read_file(file))}
            else:
                return {"data": read_file(file)}

    @classmethod
    @marshal_with(config_fields)
    def put(cls):
        args = request.get_json()
        if args is None:
            raise BadDataException("Invalid request")
        service = args.get('service', '').upper()
        data = args.get('data', None)
        app: InstallableApp = get_app_from_service(service)
        update = app.update_config_file(data, cls.relative_path(), cls.is_json())
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'update': update, **app_details}

    @classmethod
    @marshal_with(config_delete_fields)
    def delete(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        res = {'service': service, 'delete': False, 'update': False, 'state': '', 'error': ''}
        try:
            app: InstallableApp = get_app_from_service(service)
            delete = app.delete_config_file(cls.relative_path())
            app_details = get_installed_app_details(app) or {}
            res = {**res, 'delete': delete, **app_details}
        except Exception as e:
            res = {**res, 'error': str(e)}
        return res


class YmlConfigResource(ConfigResource):
    @classmethod
    def is_json(cls):
        return False

    @classmethod
    def filename(cls):
        return 'config.yml'


class LoggingResource(RubixResource):
    @classmethod
    def get(cls):
        service: str = request.args.get('service')
        if not service:
            raise BadDataException("Include ?service as an argument")
        app: InstallableApp = get_app_from_service(service)
        filename = 'logging.conf'
        directory = os.path.join(app.get_global_dir(), 'config')
        file = os.path.join(directory, filename)
        if not os.path.exists(file):
            raise NotFoundException(f'Service {service} does not have {filename}')
        return {"data": read_file(file)}

    @classmethod
    @marshal_with(config_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
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
        service = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete = app.delete_logging_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'delete': delete, **app_details}


class EnvResource(RubixResource):
    @classmethod
    def get(cls):
        service: str = request.args.get('service')
        if not service:
            raise BadDataException("Include ?service as an argument")
        app: InstallableApp = get_app_from_service(service.upper())
        filename = '.env'
        directory = os.path.join(app.get_global_dir(), 'config')
        file = os.path.join(directory, filename)
        if not os.path.exists(file):
            raise NotFoundException(f'Service {service.upper()} does not have {filename}')
        return {"data": read_file(file)}

    @classmethod
    @marshal_with(config_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
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
        service = args['service'].upper()
        app: InstallableApp = get_app_from_service(service)
        delete = app.delete_env_file()
        app_details = get_installed_app_details(app) or {}
        return {'service': service, 'delete': delete, **app_details}
