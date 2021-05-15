from copy import deepcopy

from flask_restful import fields

from src.resources.rest_schema.schema_device import device_nested_return_fields
from src.resources.utils import map_rest_schema

user_all_attributes = {
    'first_name': {
        'type': str,
        'required': True,
    },
    'last_name': {
        'type': str,
        'required': True,
    },
    'username': {
        'type': str,
        'required': True,
    },
    'password': {
        'type': str,
        'required': True,
    },
    'email': {
        'type': str,
        'required': True,
    },
}

user_return_attributes = {
    'uuid': {
        'type': str,
    },
    'first_name': {
        'type': str,
    },
    'last_name': {
        'type': str,
    },
    'username': {
        'type': str,
    },
    'email': {
        'type': str,
    },
    'role': {
        'type': str,
        'nested': True,
        'dict': 'role.value'
    },
    'state': {
        'type': str,
        'nested': True,
        'dict': 'state.value'
    }
}

user_return_fields = {}
map_rest_schema(user_return_attributes, user_return_fields)

user_all_fields = {}
map_rest_schema(user_all_attributes, user_all_fields)
map_rest_schema(user_return_attributes, user_all_fields)

user_all_fields_with_children_base = {
    'devices': fields.List(fields.Nested(device_nested_return_fields))
}
user_all_fields_with_children = deepcopy(user_return_fields)
user_all_fields_with_children.update(user_all_fields_with_children_base)
