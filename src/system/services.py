import enum


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


installation_dir = {
    'WIRES': 'wires-builds',
    'BAC_REST': 'point-server',
    'BAC_SERVER': 'bacnet-server',
    'LORA_RAW': 'lora-raw',
}

database_dir = {
    'WIRES': "/data/{}".format(installation_dir['WIRES']),
    'BAC_REST': "/data/{}".format(installation_dir['BAC_REST']),
    'BAC_SERVER': "/data/{}".format(installation_dir['BAC_SERVER']),
    'LORA_RAW': "/data/{}".format(installation_dir['LORA_RAW']),
}


def validate_installation_service(service) -> bool:
    return service in InstallableServices.__members__.keys()


def validate_service(service) -> bool:
    return service in Services.__members__.keys()


