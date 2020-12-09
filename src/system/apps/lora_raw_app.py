from src.system.apps.base.installable_app import InstallableApp


class LoRaRawApp(InstallableApp):
    def id(self) -> str:
        return 'LORA_RAW'

    def name(self) -> str:
        return 'lora-raw'

    def service_file_name(self) -> str:
        return 'nubeio-lora-raw.service'
