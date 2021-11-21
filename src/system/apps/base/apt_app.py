from abc import ABC

import gevent
from flask import current_app
from werkzeug.local import LocalProxy

from src.system.apps.base.installable_app import InstallableApp
from src.system.apps.enums.enums import Types
from src.system.utils.shell import execute_command

logger = LocalProxy(lambda: current_app.logger)


class AptApp(InstallableApp, ABC):
    @property
    def app_type(self):
        return Types.APT_APP.value

    @property
    def is_asset(self):
        return False

    def install(self) -> bool:
        logger.info('Hitting apt-get update...')
        execute_command('sudo apt-get update')
        logger.info('Installing OpenVPN Service...')
        if not execute_command('sudo apt-get install openvpn'):
            return False
        logger.info('Successfully installed OpenVPN service')
        return True

    def uninstall(self) -> bool:
        logger.info('Stopping OpenVPN Service...')
        if not execute_command('sudo systemctl disable openvpn@client && sudo systemctl stop openvpn@client'):
            return False
        logger.info('Removing OpenVPN service...')
        if not execute_command('sudo apt-get remove openvpn'):
            return False
        logger.info('OpenVPN Service is deleted.')
        return True