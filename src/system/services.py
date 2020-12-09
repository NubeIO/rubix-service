import enum


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


def validate_service(service) -> bool:
    return service in Services.__members__.keys()
