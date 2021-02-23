from src.system.apps.base.python_app import PythonApp


class BACnetServerApp(PythonApp):
    def __init__(self):
        super(BACnetServerApp, self).__init__(
            display_name='Rubix BACnet Server',
            repo_name='rubix-bacnet-server',
            service_file_name='nubeio-bacnet-server.service',
            data_dir_name='bacnet-server',
            port=1717,
            min_support_version='v1.3.0',
            description='Flask Application for Nube BACNET SERVER',
            gateway_access=True,
            url_prefix='bacnet',
            need_wires_plat=True,
        )

    @classmethod
    def service(cls) -> str:
        return 'BACNET_SERVER'

    @property
    def pre_start_sleep(self):
        return 60
