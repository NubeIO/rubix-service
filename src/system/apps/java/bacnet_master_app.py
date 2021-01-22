from src.system.apps.base.java_app import JavaApp


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
