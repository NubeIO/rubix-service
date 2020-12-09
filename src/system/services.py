import enum
import os


class InstallableServices(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    BAC_REST = 'nubeio-point-server.service'
    BAC_SERVER = 'nubeio-bacnet-server.service'
    LORA_RAW = 'nubeio-lora-raw.service'


class Services(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    BAC_REST = 'nubeio-point-server.service'
    BAC_SERVER = 'nubeio-bacnet-server.service'
    PLAT = 'nubeio-wires-plat.service'
    LORA_RAW = 'nubeio-lora-raw.service'
    LORAWAN = 'lorawan-server'
    MOSQUITTO = 'mosquitto.service'
    BBB = 'nubeio-bbio.service'
    DRAC = 'nubeio-drac.service'  # TODO


app_parent_dir = '/nube-apps/'

installation_dir = {
    'WIRES': os.path.join(app_parent_dir, 'wires-builds'),
    'BAC_REST': os.path.join(app_parent_dir, 'point-server'),
    'BAC_SERVER': os.path.join(app_parent_dir, 'bacnet-server'),
    'LORA_RAW': os.path.join(app_parent_dir, 'lora-raw'),
}


def validate_installation_service(service) -> bool:
    return service in InstallableServices.__members__.keys()


def validate_service(service) -> bool:
    return service in Services.__members__.keys()
