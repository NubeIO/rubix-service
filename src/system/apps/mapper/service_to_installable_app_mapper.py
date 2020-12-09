from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.bacnet_server_app import BACnetServerApp
from src.system.apps.lora_raw_app import LoRaRawApp
from src.system.apps.point_server_app import PointServerApp
from src.system.apps.wires_builds_app import WiresBuildsApp


def service_to_installable_app_mapper(service: str) -> InstallableApp:
    if service == "WIRES":
        return WiresBuildsApp()
    elif service == "BAC-REST":
        return PointServerApp()
    elif service == "BAC_SERVER":
        return BACnetServerApp()
    elif service == "LORA_RAW":
        return LoRaRawApp()
    raise Exception("service {} does not exist in our system".format(service))
