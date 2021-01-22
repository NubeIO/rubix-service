import enum

from flask_restful import abort

from src.system.apps.base.installable_app import InstallableApp


class Services(enum.Enum):
    LORAWAN = {'service_file_name': 'lorawan-server.service', 'display_name': 'LoRa WAN Server Service'}
    MOSQUITTO = {'service_file_name': 'mosquitto.service', 'display_name': 'Mosquitto Service'}
    BBB = {'service_file_name': 'nubeio-bbio.service', 'display_name': 'BBB IO Service'}
    DRAC = {'service_file_name': 'nubeio-drac.service', 'display_name': 'DRAC Server Service'}


class ServiceAction(enum.Enum):
    START = 1
    STOP = 2
    RESTART = 3
    DISABLE = 4
    ENABLE = 5


def validate_service(service) -> str:
    if service in Services.__members__.keys():
        return Services[service].value.get('service_file_name')
    try:
        app = InstallableApp.get_app(service, "")
        return app.service_file_name
    except ModuleNotFoundError:
        return ""


def validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart | disable | enable`')


def validate_and_create_service(action, service) -> str:
    service = service.upper()
    service_name = validate_service(service)
    if service_name:
        return "sudo systemctl {} {}".format(action, service_name)
    abort(400, message="service {} does not exist in our system".format(service))


def validate_host_restart(action) -> str:
    if action == 'restart':
        return "sudo reboot"
    abort(400, message="incorrect command to restart host try: restart {}".format(action))
