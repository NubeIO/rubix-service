from datetime import datetime

from flask_restful import reqparse, marshal_with
from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info, put_device_info, get_device_info_dict
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.platform.schema_device_info import device_info_all_attributes, device_info_all_fields


class DeviceInfoResource(RubixResource):
    parser = reqparse.RequestParser()
    for attr in device_info_all_attributes:
        parser.add_argument(attr,
                            type=device_info_all_attributes[attr]['type'],
                            required=device_info_all_attributes[attr].get('required', False),
                            help=device_info_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(device_info_all_fields)
    def get(cls):
        device_info: dict = get_device_info_dict()
        if not device_info:
            raise NotFoundException('Device info not found')
        return device_info

    @classmethod
    @marshal_with(device_info_all_fields)
    def put(cls):
        data: dict = cls.parser.parse_args()
        device_info: dict = get_device_info_dict()
        return cls.store_device_info(device_info, data)

    @classmethod
    def store_device_info(cls, device_info: dict, data: dict):
        data['updated_on'] = datetime.utcnow().isoformat()
        put_device_info(DeviceInfoModel(**{**device_info, **data}))
        return get_device_info()

    @staticmethod
    def store_device_info_if_does_not_exist():
        device_info: dict = get_device_info_dict()
        if not device_info:
            put_device_info(DeviceInfoModel())
