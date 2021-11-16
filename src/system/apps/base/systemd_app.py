import os
from abc import ABC

import gevent
from flask import current_app
from werkzeug.local import LocalProxy

from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import delete_file
from src.system.utils.shell import execute_command

logger = LocalProxy(lambda: current_app.logger)

SERVICE_DIR = '/lib/systemd/system'
SERVICE_DIR_SOFT_LINK = '/etc/systemd/system/multi-user.target.wants'


class SystemdApp(InstallableApp, ABC):
    @property
    def service_file(self) -> str:
        return os.path.join(SERVICE_DIR, self.service_file_name)

    @property
    def symlink_service_file(self):
        return os.path.join(SERVICE_DIR_SOFT_LINK, self.service_file_name)

    def create_service(self):
        raise NotImplementedError("create_service needs to be overridden")

    def install(self) -> bool:
        logger.info('Creating Linux Service...')
        lines = self.create_service()
        with open(self.service_file, "w") as file:
            file.writelines(lines)

        logger.info('Soft Un-linking Linux Service...')
        try:
            os.unlink(self.symlink_service_file)
        except FileNotFoundError as e:
            logger.info(str(e))

        logger.info('Soft Linking Linux Service...')
        os.symlink(self.service_file, self.symlink_service_file)

        logger.info('Hitting daemon-reload...')
        if not execute_command('systemctl daemon-reload'):
            return False

        logger.info('Enabling Linux Service...')
        if not execute_command('systemctl enable {}'.format(self.service_file_name)):
            return False

        """
        Some of the services takes time, coz we have sleep at starting
        So leave it on background
        """
        logger.info('Starting Linux Service...')
        gevent.spawn(execute_command, 'systemctl restart {}'.format(self.service_file_name))

        logger.info('Successfully started service')
        return True

    def uninstall(self) -> bool:
        logger.info('Stopping Linux Service...')
        if not execute_command('systemctl stop {}'.format(self.service_file_name)):
            return False

        logger.info('Un-linking Linux Service...')
        try:
            os.unlink(self.symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        logger.info('Removing Linux Service...')
        delete_file(self.service_file)

        logger.info('Hitting daemon-reload...')
        if not execute_command('systemctl daemon-reload'):
            return False
        logger.info('Service is deleted.')
        return True
