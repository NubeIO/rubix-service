import enum


class Services(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    PLAT = 'nubeio-wires-plat.service'
    LORAWAN = 'lorawan-server'
    MOSQUITTO = 'mosquitto.service'
    BBB = 'nubeio-bbio.service'
    BAC_REST = 'nubeio-bac-rest.service'
    BAC_SERVER = 'nubeio-bacnet-server.service'
    DRAC = 'nubeio-drac.service'  # TODO
