from src.system.apps.base.python_app import PythonApp


class BACnetServerApp(PythonApp):
    @classmethod
    def id(cls) -> str:
        return 'BACNET_SERVER'

    def name(self) -> str:
        return 'rubix-bacnet-server'

    def service_file_name(self) -> str:
        return 'nubeio-bacnet-server.service'

    def data_dir_name(self) -> str:
        return 'bacnet-server'

    def description(self) -> str:
        return 'Flask Application for Nube BACNET SERVER'

    def port(self) -> int:
        return 1717

    def url_prefix(self) -> str:
        return '/bacnet'

    def min_support_version(self) -> str:
        return 'v1.3.0'
