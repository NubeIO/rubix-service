import enum

from flask_restful import abort


class Services(enum.Enum):
    LORAWAN = {'service_file_name': 'lorawan-server.service', 'display_name': 'LoRa WAN Server Service'}
    MOSQUITTO = {'service_file_name': 'mosquitto.service', 'display_name': 'Mosquitto Service'}
    BBB = {'service_file_name': 'nubeio-bbio.service', 'display_name': 'BBB IO Service'}
    DRAC = {'service_file_name': 'nubeio-drac.service', 'display_name': 'DRAC Server Service'}
    NODE_RED = {'service_file_name': 'nodered.service', 'display_name': 'Node-RED Service'}
    # https://raw.githubusercontent.com/node-red/linux-installers/master/resources/nodered.service
    GRAFANA = {'service_file_name': 'grafana-server.service', 'display_name': 'Grafana Service'}
    INFLUX_DB = {'service_file_name': 'influxdb.service', 'display_name': 'Influx-DB Service'}


class ServiceAction(enum.Enum):
    START = 1
    STOP = 2
    RESTART = 3
    DISABLE = 4
    ENABLE = 5


def validate_service(service: str) -> bool:
    if service in Services.__members__.keys():
        return True
    abort(400, message="service {} does not exist in our system".format(service))


def validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    abort(400, message='action should be `start | stop | restart | disable | enable`')


def validate_host_restart(action) -> str:
    if action == 'restart':
        return "sudo reboot"
    abort(400, message="incorrect command to restart host try: `restart` not:`{}`".format(action))


def create_service_cmd(action, service_file_name) -> str:
    cmd: str = ""
    if action == "start":
        cmd = f"sudo systemctl enable {service_file_name} &&"
    elif action == "stop":
        cmd = f"sudo systemctl disable {service_file_name} &&"
    return f"{cmd} sudo systemctl {action} {service_file_name}".strip()
