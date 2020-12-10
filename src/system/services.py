import enum


class Services(enum.Enum):
    PLAT = 'nubeio-wires-plat.service'
    POINT_SERVER = 'nubeio-point-server.service'
    BACNET_SERVER = 'nubeio-bacnet-server.service'
    LORA_RAW = 'nubeio-lora-raw.service'
    WIRES = 'nubeio-rubix-wires.service'
    LORAWAN = 'lorawan-server'
    MOSQUITTO = 'mosquitto.service'
    BBB = 'nubeio-bbio.service'
    DRAC = 'nubeio-drac.service'  # TODO


def validate_service(service) -> bool:
    return service in Services.__members__.keys()
