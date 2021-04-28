from src.platform.utils import map_rest_schema

wires_plat_all_attributes = {
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

wires_plat_return_attributes = {
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

wires_plat_all_fields = {}
map_rest_schema(wires_plat_return_attributes, wires_plat_all_fields)
map_rest_schema(wires_plat_all_attributes, wires_plat_all_fields)
