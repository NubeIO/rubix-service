from src.system.services import InstallableServices

wires_domain = (
    'api.github.com',
    'NubeIO',
    'wires-builds'
)

bac_rest_domain = (
    'api.github.com',
    'NubeDev',
    'bac-rest'
)

bacnet_flask_domain = (
    'api.github.com',
    'NubeDev',
    'bacnet-flask'
)


class ServiceURL:
    def __init__(self, url, service):
        self.url = url
        self.service = service

    def _get_service_url_tuple(self):
        if self.service == InstallableServices.WIRES.name:
            return wires_domain
        elif self.service == InstallableServices.BAC_REST.name:
            return bac_rest_domain
        elif self.service == InstallableServices.BAC_SERVER.name:
            return bacnet_flask_domain

    def _check_service_url_tuple(self, service_url_tuple) -> bool:
        u = self.url.split("/")
        domain = (u[2], u[4], u[5])
        print("URL check:", domain, service_url_tuple)
        return service_url_tuple == domain

    def is_valid(self):
        service_url_tuple = self._get_service_url_tuple()
        if service_url_tuple:
            return self._check_service_url_tuple(service_url_tuple)
        else:
            return False
