from src.platform.schema_wires_plat import map_rest_schema

users_all_attributes = {
    'user_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'password': {
        'type': str,
        'required': True,
        'help': '',
    },
}

users_return_attributes = {
    'user_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'password': {
        'type': str,
        'required': True,
        'help': '',
    },
    'created_on': {
        'type': str,
        'help': '',
    },
    'updated_on': {
        'type': str,
        'help': '',
    },
}

users_all_fields = {}
map_rest_schema(users_return_attributes, users_all_fields)
map_rest_schema(users_all_attributes, users_all_fields)
