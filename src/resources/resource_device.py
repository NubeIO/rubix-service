import uuid as uuid_

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.device.model_device import DeviceModel
from src.resources.rest_schema.schema_device import device_all_attributes, device_return_fields


class DeviceResourceList(RubixResource):
    parser = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser.add_argument(attr,
                            type=device_all_attributes[attr]['type'],
                            required=device_all_attributes[attr].get('required', False),
                            help=device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(device_return_fields)
    def get(cls):
        return DeviceModel.find_all()

    @classmethod
    @marshal_with(device_return_fields)
    def post(cls):
        args = cls.parser.parse_args()
        uuid = str(uuid_.uuid4())
        device = DeviceModel(uuid=uuid, **args)
        device.save_to_db()
        return device


class DeviceResourceByUUID(RubixResource):
    @classmethod
    @marshal_with(device_return_fields)
    def get(cls, uuid):
        device: DeviceModel = DeviceModel.find_by_uuid(uuid)
        if device is None:
            raise NotFoundException('Device not found')
        return device

    @classmethod
    @marshal_with(device_return_fields)
    def patch(cls, uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('device_id', type=str, required=False, store_missing=False)
        args = parser.parse_args()
        device: DeviceModel = DeviceModel.find_by_uuid(uuid)
        if device is None:
            raise NotFoundException("Device not found")
        device.update(**args)
        return device

    @classmethod
    def delete(cls, uuid):
        device: DeviceModel = DeviceModel.find_by_uuid(uuid)
        device.delete_from_db()
        return {'message': 'Device has been deleted successfully'}
