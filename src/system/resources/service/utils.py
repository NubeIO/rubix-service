import enum
import json
from datetime import datetime, timedelta

from flask import current_app
from rubix_http.exceptions.exception import NotFoundException

from src import AppSetting
from src.system.utils.file import write_file, read_file


class Services(enum.Enum):
    LORAWAN = {'service_file_name': 'lorawan-server.service', 'display_name': 'LoRa WAN Server Service'}
    LORAWAN_GATEWAY = {'service_file_name': 'lorawan-gateway.service', 'display_name': 'LoRa WAN Gateway Service'}
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
    raise NotFoundException(f'service {service} does not exist in our system')


def validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    raise NotFoundException('action should be `start | stop | restart | disable | enable`')


def validate_host_restart(action) -> str:
    if action == 'restart':
        return "reboot"
    raise NotFoundException(f'incorrect command to restart host try: `restart` not:`{action}`')


def create_service_cmd(action, service_file_name) -> str:
    cmd: str = ""
    if action == "start":
        cmd = f"systemctl enable {service_file_name} &&"
    elif action == "stop":
        cmd = f"systemctl disable {service_file_name} &&"
    return f"{cmd} systemctl {action} {service_file_name}".strip()


def get_service_restart_job(service) -> dict:
    service_schedule_restarts: dict = get_service_restart_jobs()
    return service_schedule_restarts.get(service, {})


def get_service_restart_jobs() -> dict:
    app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    return json.loads(read_file(app_setting.service_restart_job_file) or "{}")


def create_service_restart_job(data: dict):
    app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    service_schedule_restarts: dict = get_service_restart_jobs()
    service_schedule_restarts.update(data)
    write_file(app_setting.service_restart_job_file, json.dumps(service_schedule_restarts, indent=2))


def delete_service_restart_job(service: str):
    app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    service_schedule_restarts: dict = get_service_restart_jobs()
    service_schedule_restarts.pop(service)
    write_file(app_setting.service_restart_job_file, json.dumps(service_schedule_restarts, indent=2))
