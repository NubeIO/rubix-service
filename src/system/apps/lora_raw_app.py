from src.system.apps.base.python_app import PythonApp


class LoRaRawApp(PythonApp):
    def __init__(self):
        super(LoRaRawApp, self).__init__(
            repo_name='lora-raw',
            service_file_name='nubeio-lora-raw.service',
            data_dir_name='lora-raw',
            port=1919,
            min_support_version='v1.1.0',
            description='NubeIO LoRa Raw pyserial',
            gateway_access=True,
            url_prefix='/lora',
        )

    @classmethod
    def id(cls) -> str:
        return 'LORA_RAW'
