from src.system.apps.base.python_app import PythonApp


class PointServerApp(PythonApp):
    @classmethod
    def id(cls) -> str:
        return 'POINT_SERVER'

    def name(self) -> str:
        return 'rubix-point-server'

    def service_file_name(self) -> str:
        return 'nubeio-point-server.service'

    def data_dir_name(self) -> str:
        return 'point-server'

    def port(self) -> int:
        return 1515

    def url_prefix(self) -> str:
        return '/ps'

    def min_support_version(self) -> str:
        return 'v1.2.0'
