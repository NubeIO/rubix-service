from datetime import datetime, timedelta

from flask import request
from rubix_http.exceptions.exception import BadDataException, NotFoundException
from rubix_http.resource import RubixResource

from src.system.resources.rest_schema.schema_restart_job import restart_job_attributes, restart_job_delete_attributes
from src.system.resources.service.utils import create_service_restart_job, Services, create_service_cmd, \
    delete_service_restart_job
from src.system.utils.data_validation import validate_args


class ServiceRestartJob(RubixResource):
    @classmethod
    def post(cls):
        args = request.get_json()
        if not validate_args(args, restart_job_attributes):
            raise BadDataException('Invalid request')
        restart_res = []
        for arg in args:
            service: str = arg['service'].upper()
            timer: int = arg['timer']
            res = {'service': service, 'timer': timer, 'error': ''}
            try:
                cmd: str = cls.validate_and_create_restart_service_cmd(arg['service'].upper())
                restart_job: dict = {
                    service: {
                        "timer": timer,
                        "cmd": cmd,
                        "prev_time": str(datetime.now()),
                        "next_time": str(datetime.now() + timedelta(minutes=timer))
                    }
                }
                create_service_restart_job(restart_job)
            except Exception as e:
                res = {**res, 'error': str(e)}
            restart_res.append(res)
        return restart_res

    @classmethod
    def delete(cls):
        args = request.get_json()
        if not validate_args(args, restart_job_delete_attributes):
            raise BadDataException('Invalid request')
        restart_res = []
        for arg in args:
            service: str = arg['service'].upper()
            res = {'service': service, 'error': ''}
            try:
                cls.validate_service(service)
                delete_service_restart_job(service)
            except Exception as e:
                res = {**res, 'error': str(e)}
            restart_res.append(res)
        return restart_res

    @classmethod
    def validate_and_create_restart_service_cmd(cls, service: str) -> str:
        if service in Services.__members__.keys():
            service_file_name = Services[service].value.get('service_file_name')
            return create_service_cmd("restart", service_file_name)
        raise NotFoundException(f'service {service} does not exist in our system')

    @classmethod
    def validate_service(cls, service: str):
        if service not in Services.__members__.keys():
            raise NotFoundException(f'service {service} does not exist in our system')
