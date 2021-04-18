import json
from typing import Dict

from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException, BadDataException

from src.discover.remote_device_registry import RemoteDeviceRegistry
from src.slaves.resources.slaves_base import SlavesBase
from src.system.utils.file import write_file


class SlavesPlural(SlavesBase):

    @classmethod
    def get(cls):
        return cls.get_slaves()[0]

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('global_uuid', type=str)
        args = parser.parse_args()
        global_uuid = args['global_uuid']
        device: Dict = RemoteDeviceRegistry().devices[global_uuid]
        if global_uuid not in RemoteDeviceRegistry().devices and device:
            raise NotFoundException(f"global_uuid = {global_uuid} does not exist on discovered devices list")
        slaves, slaves_file = cls.get_slaves()
        if global_uuid in slaves:
            raise BadDataException(f"global_uuid = {global_uuid} is already inserted")
        slaves[global_uuid] = device
        write_file(slaves_file, json.dumps(slaves))
        return slaves
