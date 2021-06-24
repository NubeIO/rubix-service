import json

from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import put_device_info, get_device_info

from src.system.utils.file import read_file


def upgrade_001():
    device_info = json.loads(read_file('/data/rubix-registry/wires-plat.json') or "{}")
    if device_info and not get_device_info():
        put_device_info(DeviceInfoModel(**device_info))
