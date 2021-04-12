import logging
from typing import List, Dict

from mrb.mapper import api_to_slaves_broadcast_topic_mapper

from src.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class RemoteDeviceRegistry(metaclass=Singleton):
    def __init__(self):
        self.__devices: List[Dict[str, str]] = []
        self.__available_devices_global_uuids: List[str] = []

    @property
    def devices(self) -> List[Dict[str, str]]:
        return self.__devices

    @property
    def available_devices_global_uuids(self) -> List[str]:
        return self.__available_devices_global_uuids

    def register(self):
        logger.info(f"Called devices registration")
        while True:
            self.poll_devices()

    def poll_devices(self):
        """
        We don't need to sleep the response itself has sleep of bridge timeout seconds
        """
        devices: dict = api_to_slaves_broadcast_topic_mapper('/api/wires/plat').content
        temp_devices: List[Dict[str, str]] = []
        available_devices_global_uuids: List[str] = []
        for device in devices:
            temp_devices.append(devices[device])
            available_devices_global_uuids.append(device)

        self.__devices = temp_devices
        self.__available_devices_global_uuids = available_devices_global_uuids
