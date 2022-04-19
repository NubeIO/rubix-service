from flask_restful import fields

from src.platform.utils import map_rest_schema
from src.system.resources.rest_schema.schema_reboot_job import reboot_all_fields

device_info_all_attributes = {
    'client_id': {
        'type': str,
        'required': True,
    },
    'client_name': {
        'type': str,
        'required': True,
    },
    'site_id': {
        'type': str,
        'required': True,
    },
    'site_name': {
        'type': str,
        'required': True,
    },
    'device_id': {
        'type': str,
        'required': True,
    },
    'device_name': {
        'type': str,
        'required': True,
    },
    'device_type': {
        'type': str,
        'required': True,
    },
    'site_address': {
        'type': str,
        'required': True,
    },
    'site_city': {
        'type': str,
        'required': True,
    },
    'site_state': {
        'type': str,
        'required': True,
    },
    'site_zip': {
        'type': str,
        'required': True,
    },
    'site_country': {
        'type': str,
        'required': True,
    },
    'site_lat': {
        'type': str,
        'required': True,
    },
    'site_lon': {
        'type': str,
        'required': True,
    },
    'time_zone': {
        'type': str,
        'required': True,
    },
}

device_info_return_attributes = {
    'global_uuid': {
        'type': str,
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    }
}

device_info_all_fields = {}
map_rest_schema(device_info_return_attributes, device_info_all_fields)
map_rest_schema(device_info_all_attributes, device_info_all_fields)

device_info_all_fields_with_reboot_job = {**device_info_all_fields, 'reboot_job': fields.Nested(reboot_all_fields)}
