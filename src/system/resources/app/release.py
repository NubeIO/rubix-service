import json

import requests
from flask_restful import Resource

from src.system.resources.app.utils import get_app_from_service


class ReleaseResource(Resource):
    def get(self, service):
        service = service.upper()
        app = get_app_from_service(service)
        resp = requests.get(app.get_releases_link())
        data = json.loads(resp.content)
        releases = []
        for row in data:
            releases.append(row.get('tag_name'))
        return releases
