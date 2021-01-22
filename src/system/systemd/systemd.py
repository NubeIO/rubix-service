import os
from abc import ABC, abstractmethod

from src.pyinstaller import resource_path
from src.system.utils.file import delete_file
from src.system.utils.shell import execute_command

SERVICE_DIR = '/lib/systemd/system'
SERVICE_DIR_SOFT_LINK = '/etc/systemd/system/multi-user.target.wants'


class Systemd(ABC):
    def __init__(self, service_file_name):
        self.__service_file_name = service_file_name
        self.__service_file = os.path.join(SERVICE_DIR, self.__service_file_name)
        self.__symlink_service_file = os.path.join(SERVICE_DIR_SOFT_LINK, self.__service_file_name)

    def install(self) -> bool:

        print('Creating Linux Service...')
        lines = self.create_service()
        with open(self.__service_file, "w") as file:
            file.writelines(lines)

        print('Soft Un-linking Linux Service...')
        try:
            os.unlink(self.__symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        print('Soft Linking Linux Service...')
        os.symlink(self.__service_file, self.__symlink_service_file)

        print('Hitting daemon-reload...')
        if not execute_command('sudo systemctl daemon-reload'):
            return False

        print('Enabling Linux Service...')
        if not execute_command('sudo systemctl enable {}'.format(self.__service_file_name)):
            return False

        print('Starting Linux Service...')
        if not execute_command('sudo systemctl restart {}'.format(self.__service_file_name)):
            return False

        print('Successfully started service')
        return True

    def uninstall(self) -> bool:
        print('Stopping Linux Service...')
        if not execute_command('systemctl stop {}'.format(self.__service_file_name)):
            return False

        print('Un-linking Linux Service...')
        try:
            os.unlink(self.__symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        print('Removing Linux Service...')
        delete_file(self.__service_file)

        print('Hitting daemon-reload...')
        if not execute_command('sudo systemctl daemon-reload'):
            return False
        print('Service is deleted.')
        return True

    def restart(self) -> bool:
        print('Restarting Linux Service...')
        if not execute_command('sudo systemctl restart {}'.format(self.__service_file_name)):
            return False
        print('Successfully restarted service')
        return True

    @abstractmethod
    def create_service(self):
        raise NotImplementedError('Need to be implemented')


class AppSystemd(Systemd):
    def __init__(self, service_file_name, pre_start_sleep=0, wd=None, port=None, data_dir=None, name=None,
                 description=None):
        super().__init__(service_file_name)
        self.__pre_start_sleep = pre_start_sleep
        self.__wd = wd
        self.__port = port
        self.__data_dir = data_dir
        self.__name = name
        self.__description = description

    def create_service(self):
        lines = []
        with open(resource_path('systemd/nubeio-app-service.service')) as systemd_file:
            for line in systemd_file.readlines():
                if '<pre_start_sleep>' in line:
                    line = line.replace('<pre_start_sleep>', str(self.__pre_start_sleep))
                if '<working_dir>' in line and self.__wd:
                    line = line.replace('<working_dir>', self.__wd)
                if '<port>' in line and self.__port:
                    line = line.replace('<port>', str(self.__port))
                if '<data_dir>' in line and self.__data_dir:
                    line = line.replace('<data_dir>', self.__data_dir)
                if '<name>' in line and self.__name:
                    line = line.replace('<name>', self.__name)
                if '<description>' in line and self.__description:
                    line = line.replace('<description>', self.__description)
                lines.append(line)
        return lines
