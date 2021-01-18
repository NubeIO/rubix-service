from src.platform.schema_wires_plat import map_rest_schema

users_all_attributes = {
    'username': {
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
    'username': {
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

user_token_attributes = {
    'access_token': {
        'type': str,
        'required': True,
        'help': '',
    },
    'token_type': {
        'type': str,
        'required': True,
        'help': '',
    },
}

users_all_fields = {}
users_return_fields ={}
users_token_fields = {}

map_rest_schema(users_all_attributes, users_all_fields)
map_rest_schema(users_return_attributes, users_return_fields)
map_rest_schema(user_token_attributes, users_token_fields)
