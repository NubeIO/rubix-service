import logging
import threading
from typing import List, Dict, Union

import gevent
from mrb.mapper import api_to_slaves_broadcast_topic_mapper
from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info

from src import AppSetting
from src.slaves.resources.slaves_base import SlavesBase
from src.utils.singleton import Singleton

logger = logging.getLogger(__name__)

MIN_LOOP_TO_SHOW_ONLINE: int = 5

device_info: Union[DeviceInfoModel, None] = get_device_info()


class RemoteDeviceRegistry(metaclass=Singleton):
    def __init__(self):
        self.__app_setting: Union[AppSetting, None] = None
        self.__temp_devices: Dict[str, Dict] = {}
        self.__total_count: Dict[str, int] = {}
        self.__failure_count: Dict[str, int] = {}
        self.__devices: Dict[str, Dict] = {}
        self.__available_inserted_devices_global_uuids: List[str] = []
        self.__sem = threading.Semaphore()

    @property
    def devices(self) -> Dict[str, Dict]:
        return self.__devices

    @property
    def total_count(self) -> Dict[str, int]:
        return self.__total_count

    @property
    def failure_count(self) -> Dict[str, int]:
        return self.__failure_count

    @property
    def available_inserted_devices_global_uuids(self) -> List[str]:
        return self.__available_inserted_devices_global_uuids

    @property
    def sem(self):
        return self.__sem

    def register(self, app_setting: AppSetting):
        logger.info(f"Called devices registration")
        self.__app_setting = app_setting
        while True:
            self.poll_devices()
            gevent.sleep(50)

    def poll_devices(self):
        """
        We don't need to sleep the response itself has sleep of bridge timeout seconds
        """
        RemoteDeviceRegistry().sem.acquire()
        active_slave_devices: Dict[str, Dict] = api_to_slaves_broadcast_topic_mapper('/api/wires/plat',
                                                                                     timeout=10).content
        RemoteDeviceRegistry().sem.release()
        for global_uuid in active_slave_devices:
            active_slave_device = active_slave_devices[global_uuid]
            device_info_model: DeviceInfoModel = device_info
            self.__temp_devices[global_uuid] = {
                **active_slave_device,
                'is_master': global_uuid == device_info_model.global_uuid,
                'consecutive_success_count':
                    self.__temp_devices.get(global_uuid, {}).get('consecutive_success_count', 0) + 1
            }
        available_inserted_devices_global_uuids: List[str] = []
        slaves: Dict[str, Dict] = SlavesBase.get_slaves_by_app_setting(self.__app_setting)[0]

        for global_uuid in slaves:
            self.__total_count[global_uuid] = self.__total_count.get(global_uuid, 0) + 1
            if global_uuid not in active_slave_devices:
                self.__failure_count[global_uuid] = self.__failure_count.get(global_uuid, 0) + 1

        global_uuids: List[str] = list(self.__temp_devices.keys())
        for global_uuid in global_uuids:
            if global_uuid not in active_slave_devices:
                temp_device = self.__temp_devices[global_uuid]
                logger.warning(f'Deleting global_uuid={global_uuid}, device_name={temp_device.get("device_name")}, '
                               f'consecutive_success_count={temp_device.get("consecutive_success_count")}')
                del self.__temp_devices[global_uuid]

        devices: Dict[str, Dict] = {}
        for global_uuid in active_slave_devices:
            temp_device: dict = self.__temp_devices[global_uuid]
            if temp_device.get('consecutive_success_count') >= MIN_LOOP_TO_SHOW_ONLINE or self.failure_count.get(
                    global_uuid, 0) == 0:
                devices[global_uuid] = temp_device
                if global_uuid in slaves:
                    available_inserted_devices_global_uuids.append(global_uuid)

        logger.info(f'Available devices count: {len(available_inserted_devices_global_uuids)}')
        self.__devices = devices
        self.__available_inserted_devices_global_uuids = available_inserted_devices_global_uuids
