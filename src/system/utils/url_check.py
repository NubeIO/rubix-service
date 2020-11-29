wires_domain = (
    'api.github.com',
    'NubeIO',
    'wires-builds'
)

bac_rest_domain = (
    'github',
    'NubeDev',
    'bac-rest'
)

bacnet_flask_domain = (
    'api.github.com',
    'NubeDev',
    'bacnet-flask'
)

service_urls = {
    'WIRES': 'https://api.github.com/repos/NubeIO/wires-builds/releases',
    'BAC_REST': 'https://api.github.com/repos/NubeDev/bac-rest/releases',
    'BAC_SERVER': 'https://api.github.com/repos/NubeDev/bacnet-flask/releases'
}


class IsValidURL:
    def __init__(self, url, service):
        self.url = url
        self.service = service

    def service_to_url(self):
        if self.service == 'WIRES':
            return wires_domain
        elif self.service == 'BAC_REST':
            return bac_rest_domain
        elif self.service == 'BAC_SERVER':
            return bacnet_flask_domain

    def check_url(self, url_to_check):
        u = self.url.split("/")
        domain = (u[2], u[4], u[5])
        print(domain, url_to_check)
        if url_to_check == domain:
            return True
        else:
            return False
