from abc import ABC

from flask import current_app
from werkzeug.local import LocalProxy

from src.pyinstaller import resource_path
from src.system.apps.base.systemd_app import SystemdApp
from src.system.apps.enums.enums import Types

logger = LocalProxy(lambda: current_app.logger)


class GoApp(SystemdApp, ABC):
    @property
    def app_type(self):
        return Types.GO_APP.value

    @property
    def select_in(self) -> bool:
        return True

    @property
    def select_in_content(self) -> str:
        return "flow-framework"

    # noinspection DuplicatedCode
    def create_service(self):
        lines = []
        with open(resource_path('systemd/nubeio-app-go-service.service')) as systemd_file:
            wd: str = self.get_wd()
            global_dir: str = self.get_global_dir()
            for line in systemd_file.readlines():
                if '<pre_start_sleep>' in line:
                    line = line.replace('<pre_start_sleep>', str(self.pre_start_sleep))
                if '<working_dir>' in line and wd:
                    line = line.replace('<working_dir>', wd)
                if '<port>' in line and self.port:
                    line = line.replace('<port>', str(self.port))
                if '<global_dir>' in line and global_dir:
                    line = line.replace('<global_dir>', global_dir)
                if '<name>' in line and self.repo_name:
                    line = line.replace('<name>', self.repo_name)
                if '<description>' in line and self.description:
                    line = line.replace('<description>', self.description)
                lines.append(line)
        return lines
