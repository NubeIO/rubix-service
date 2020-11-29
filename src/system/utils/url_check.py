wires_domain = (
    'api.github.com',
    'NubeIO',
    'wires-builds',
    'zipball'
)

bac_rest_domain = (
    'github',
    'NubeDev',
    'bac-rest',
    'zipball'
)

bacnet_flask_domain = (
    'api.github.com',
    'NubeDev',
    'bacnet-flask',
    'zipball'
)


class IsValidURL:
    def __init__(self, url, url_to_check):
        self.url = url
        self.url_to_check = url_to_check

    def check_url(self):
        u = self.url.split("/")
        domain = (u[2], u[4], u[5], u[6])
        if self.url_to_check == domain:
            return True
        else:
            return False
