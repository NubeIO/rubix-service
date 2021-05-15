from src.resources.utils import map_rest_schema

device_all_attributes = {
    'device_id': {
        'type': str,
        'required': True,
    },
}

device_return_attributes = {
    'uuid': {
        'type': str,
    },
    'user_uuid': {
        'type': str,
    },
    'device_id': {
        'type': str,
    },
}

device_nested_return_attributes = {
    'uuid': {
        'type': str,
    },
    'device_id': {
        'type': str,
    },
}

device_return_fields = {}
map_rest_schema(device_return_attributes, device_return_fields)

device_nested_return_fields = {}
map_rest_schema(device_nested_return_attributes, device_nested_return_fields)

device_all_fields = {}
map_rest_schema(device_all_attributes, device_all_fields)
map_rest_schema(device_return_attributes, device_all_fields)
