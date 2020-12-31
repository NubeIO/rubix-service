from src.system.apps.base.python_app import PythonApp


class LoRaRawApp(PythonApp):
    @classmethod
    def id(cls) -> str:
        return 'LORA_RAW'

    def name(self) -> str:
        return 'lora-raw'

    def service_file_name(self) -> str:
        return 'nubeio-lora-raw.service'

    def data_dir_name(self) -> str:
        return 'lora-raw'

    def port(self) -> int:
        return 1919

    def url_prefix(self) -> str:
        return '/lora'

    def min_support_version(self) -> str:
        return 'v1.1.0'
