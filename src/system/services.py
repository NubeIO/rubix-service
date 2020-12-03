import enum


class InstallableServices(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    BAC_REST = 'nubeio-bac-rest.service'
    BAC_SERVER = 'nubeio-bacnet-server.service'


class Services(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    BAC_REST = 'nubeio-bac-rest.service'
    BAC_SERVER = 'nubeio-bacnet-server.service'
    PLAT = 'nubeio-wires-plat.service'
    LORAWAN = 'lorawan-server'
    MOSQUITTO = 'mosquitto.service'
    BBB = 'nubeio-bbio.service'
    DRAC = 'nubeio-drac.service'  # TODO


def validate_installation_service(service) -> bool:
    return service in InstallableServices.__members__.keys()


def validate_service(service) -> bool:
    return service in Services.__members__.keys()
