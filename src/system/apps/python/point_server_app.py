from src.system.apps.base.python_app import PythonApp


class PointServerApp(PythonApp):
    def __init__(self):
        super(PointServerApp, self).__init__(
            display_name='Rubix Point Server',
            repo_name='rubix-point-server',
            service_file_name='nubeio-point-server.service',
            data_dir_name='point-server',
            port=1515,
            min_support_version='v1.4.2',
            description='Flask Application for Nube Rest API',
            gateway_access=True,
            url_prefix='ps',
        )

    @classmethod
    def service(cls) -> str:
        return 'POINT_SERVER'
