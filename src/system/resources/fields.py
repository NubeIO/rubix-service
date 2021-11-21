from flask_restful import fields

from src.system.utils.shell import States

restart_job_fields = {
    "timer": fields.Integer,
    "error": fields.String
}

service_fields = {
    'display_name': fields.String,
    'service': fields.String,
    'is_installed': fields.Boolean,
    'state': fields.String(default=States.INACTIVE.value),
    'status': fields.Boolean(default=False),
    'date_since': fields.String,
    'time_since': fields.String,
    'is_enabled': fields.Boolean(default=False),
    'restart_job': fields.Nested(restart_job_fields)
}

config_fields = {
    'service': fields.String,
    'update': fields.Boolean,
    'state': fields.String(default=States.INACTIVE.value)
}

config_delete_fields = {
    **config_fields,
    'error': fields.String
}
