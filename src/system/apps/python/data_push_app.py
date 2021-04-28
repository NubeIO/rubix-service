from src.system.apps.base.python_app import PythonApp


class DataPushApp(PythonApp):
    def __init__(self):
        super(DataPushApp, self).__init__(
            display_name='Data Push Service',
            repo_name='rubix-data-push',
            service_file_name='nubeio-data-push.service',
            data_dir_name='data-push',
            port=2020,
            min_support_version='v0.1.0',
            description='NubeIO Data Push Service',
            gateway_access=True,
            url_prefix='dp',
        )

    @classmethod
    def service(cls) -> str:
        return 'DATA_PUSH'
