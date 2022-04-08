from src.platform.utils import map_rest_schema

reboot_job_attributes = {
    'timer': {
        'type': int,
        'required': True
    }
}

reboot_job_return_attributes = {
    'error': {
        'type': str,
    },
}

reboot_all_fields = {}
map_rest_schema(reboot_job_attributes, reboot_all_fields)
map_rest_schema(reboot_job_return_attributes, reboot_all_fields)
