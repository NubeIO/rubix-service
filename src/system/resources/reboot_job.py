from datetime import datetime, timedelta

from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import BadDataException
from rubix_http.resource import RubixResource

from src.system.resources.rest_schema.schema_reboot_job import reboot_job_attributes, reboot_all_fields
from src.system.resources.service.utils import create_reboot_job, get_reboot_job


class RebootJob(RubixResource):
    parser = reqparse.RequestParser()
    for attr in reboot_job_attributes:
        parser.add_argument(attr,
                            type=reboot_job_attributes[attr]['type'],
                            required=reboot_job_attributes[attr].get('required', False),
                            help=reboot_job_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(reboot_all_fields)
    def get(cls):
        return get_reboot_job()

    @classmethod
    @marshal_with(reboot_all_fields)
    def post(cls):
        args: dict = cls.parser.parse_args()
        timer = args['timer']
        if timer < 10:
            raise BadDataException('Invalid timer, timer needs to be greater than or equal to 10')
        job: dict = {
            "timer": timer,
            "prev_time": str(datetime.now()),
            "next_time": str(datetime.now() + timedelta(minutes=timer))
        }
        return create_reboot_job(job)

    @classmethod
    def delete(cls):
        create_reboot_job({})
        return '', 204
