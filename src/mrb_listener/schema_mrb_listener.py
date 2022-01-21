from src.platform.utils import map_rest_schema

mrb_listener_all_attributes = {
    'enabled': {
        'type': bool,
    },
    'master': {
        'type': bool,
    },
    'name': {
        'type': str,
    },
    'host': {
        'type': str,
    },
    'port': {
        'type': int,
    },
    'ssl': {
        'type': bool,
    },
    'authentication': {
        'type': bool,
    },
    'username': {
        'type': str,
    },
    'password': {
        'type': str,
    },
    'keepalive': {
        'type': int,
    },
    'qos': {
        'type': int,
    },
    'retain': {
        'type': bool,
    },
    'attempt_reconnect_on_unavailable': {
        'type': bool,
    },
    'attempt_reconnect_secs': {
        'type': int,
    },
    'timeout': {
        'type': int,
    },
}

mrb_listener_all_fields = {}
map_rest_schema(mrb_listener_all_attributes, mrb_listener_all_fields)
