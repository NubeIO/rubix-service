from typing import Union

from flask_restful import fields
from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info_dict, get_device_info

DEFAULT_DEVICE_TYPE = 'rubix-compute'


def get_field_type(attr_type):
    if attr_type == int:
        return fields.Integer()
    elif attr_type == str:
        return fields.String()
    elif attr_type == bool:
        return fields.Boolean()
    elif attr_type == float:
        return fields.Float()


def map_rest_schema(schema, resource_fields):
    """
    Adds schema dict marshaled data to resource_fields dict
    """
    for attr in schema:
        # hack fix... change to make fields primary thing and switch get_field_type to return opposite
        if not isinstance(schema[attr]['type'], fields.Raw):
            resource_fields[attr] = get_field_type(schema[attr]['type'])
        else:
            resource_fields[attr] = schema[attr]['type']
        if schema[attr].get('nested', False):
            resource_fields[attr].__init__(attribute=schema[attr]['dict'])


def get_device_info_dict_with_defaults() -> Union[dict, None]:
    device_info: dict = get_device_info_dict()
    if not device_info:
        return None
    if not device_info.get('device_type'):
        device_info = {**device_info, 'device_type': DEFAULT_DEVICE_TYPE}
    return device_info


def get_device_info_with_defaults() -> Union[DeviceInfoModel, None]:
    device_info: DeviceInfoModel = get_device_info()
    if not device_info:
        return None
    if not device_info.device_type:
        device_info.device_type = DEFAULT_DEVICE_TYPE
    return device_info
