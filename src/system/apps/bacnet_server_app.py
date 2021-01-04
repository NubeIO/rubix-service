from src.system.apps.base.python_app import PythonApp


class BACnetServerApp(PythonApp):
    def __init__(self):
        super(BACnetServerApp, self).__init__(
            repo_name='rubix-bacnet-server',
            service_file_name='nubeio-bacnet-server.service',
            data_dir_name='bacnet-server',
            port=1717,
            min_support_version='v1.3.0',
            description='Flask Application for Nube BACNET SERVER',
            gateway_access=True,
            url_prefix='/bacnet',
        )

    @classmethod
    def id(cls) -> str:
        return 'BACNET_SERVER'
