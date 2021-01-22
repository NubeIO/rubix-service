import os

from flask import current_app
from werkzeug.local import LocalProxy

from src.system.apps.base.java_app import JavaApp

logger = LocalProxy(lambda: current_app.logger)


class BACnetMasterApp(JavaApp):
    def __init__(self):
        super(BACnetMasterApp, self).__init__(
            display_name='BACnet Master',
            repo_name='iot-engine',
            service_file_name='nubeio-bacnet-server.service',
            data_dir_name='bacnet-master',
            port=8888,
            min_support_version='v0.2.0',
            description='BACnet Master for BACnet discovery',
            gateway_access=True,
            url_prefix='/bm',
        )

    @classmethod
    def service(cls) -> str:
        return 'BACNET_MASTER'

    @property
    def name_contains(self) -> str:
        return 'bacnet'

    def create_service(self):
        lines = []
        with open(os.path.join(self.get_wd(), 'conf/nubeio-bacnet.service')) as systemd_file:
            wd: str = self.get_wd()
            for line in systemd_file.readlines():
                if '/app/bacnet' in line:
                    line = line.replace('/app/bacnet', wd)
                lines.append(line)
        return lines
