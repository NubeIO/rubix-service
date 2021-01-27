from flask_restful import fields

from src.system.utils.shell import States

service_fields = {
    'display_name': fields.String,
    'service': fields.String,
    'is_installed': fields.Boolean,
    'state': fields.String(default=States.INACTIVE.value),
    'status': fields.Boolean(default=False),
    'date_since': fields.String,
    'time_since': fields.String,
}
