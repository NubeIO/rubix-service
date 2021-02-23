from src.system.apps.base.python_app import PythonApp


class LoRaRawApp(PythonApp):
    def __init__(self):
        super(LoRaRawApp, self).__init__(
            display_name='LoRa Raw',
            repo_name='lora-raw',
            service_file_name='nubeio-lora-raw.service',
            data_dir_name='lora-raw',
            port=1919,
            min_support_version='v1.1.0',
            description='NubeIO LoRa Raw pyserial',
            gateway_access=True,
            url_prefix='lora',
            need_wires_plat=True,
        )

    @classmethod
    def service(cls) -> str:
        return 'LORA_RAW'
