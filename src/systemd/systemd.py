import inspect
import os
from abc import ABC, abstractmethod

from src.system.utils.shell_commands import execute_command

SERVICE_DIR = '/lib/systemd/system'
SERVICE_DIR_SOFT_LINK = '/etc/systemd/system/multi-user.target.wants'
SERVICE_NAME = 'nubeio-rubix-service.service'


class SystemdCreator(ABC):
    def create_service(self):
        service_file = os.path.join(SERVICE_DIR, SERVICE_NAME)
        symlink_service_file = os.path.join(SERVICE_DIR_SOFT_LINK, SERVICE_NAME)

        lines = self.edit_service()
        with open(service_file, "w") as file:
            file.writelines(lines)

        print('Soft Un-linking Linux Service...')
        try:
            os.unlink(symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        print('Soft Linking Linux Service...')
        os.symlink(service_file, symlink_service_file)

        print('Hitting daemon-reload...')
        execute_command('sudo systemctl daemon-reload')

        print('Enabling Linux Service...')
        execute_command('sudo systemctl enable {}'.format(SERVICE_NAME))

        print('Starting Linux Service...')
        execute_command('sudo systemctl restart {}'.format(SERVICE_NAME))

    @abstractmethod
    def edit_service(self):
        raise NotImplementedError('Need to be implemented')


class RubixServiceSystemdCreator(SystemdCreator):
    def __init__(self, wd, port, data_dir, global_dir, artifact_dir, token):
        self.__wd = wd
        self.__port = port
        self.__data_dir = data_dir
        self.__global_dir = global_dir
        self.__artifact_dir = artifact_dir
        self.__token = token

    @staticmethod
    def template():
        return inspect.cleandoc("""
            [Unit]
            Description=Flask Application for Nube System Monitoring
            After=network.target

            [Service]
            Type=simple
            User=root
            WorkingDirectory=<working_dir>
            ExecStart=<working_dir>/rubix-service -p <port> -d <data_dir> -g <global_dir> -a <artifact_dir> --token <token> --prod
            Restart=always
            RestartSec=10
            StandardOutput=syslog
            StandardError=syslog
            SyslogIdentifier=rubix-service

            [Install]
            WantedBy=multi-user.target
            """).split("\n")

    def edit_service(self):
        print('Creating Linux Service...')
        lines = []
        for line in RubixServiceSystemdCreator.template():
            if '<working_dir>' in line:
                line = line.replace('<working_dir>', self.__wd)
            if '<port>' in line:
                line = line.replace('<port>', str(self.__port))
            if '<data_dir>' in line:
                line = line.replace('<data_dir>', self.__data_dir)
            if '<global_dir>' in line:
                line = line.replace('<global_dir>', self.__global_dir)
            if '<artifact_dir>' in line:
                line = line.replace('<artifact_dir>', self.__artifact_dir)
            if ' --token <token>' in line:
                token = self.__token
                line = line.replace(' --token <token>', '' if token is None else ' --token {}'.format(token))
            lines.append('{}\n'.format(line))
        return lines
