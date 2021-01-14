import json

import requests
from flask_restful import Resource
from packaging import version

from src.system.resources.app.utils import get_app_from_service
from src.users.authorize_users import authorize


class ReleaseResource(Resource):
    @authorize
    def get(self, service):
        service = service.upper()
        app = get_app_from_service(service)
        resp = requests.get(app.get_releases_link())
        data = json.loads(resp.content)
        releases = []
        for row in data:
            if version.parse(app.min_support_version) <= version.parse(row.get('tag_name')):
                releases.append(row.get('tag_name'))
        return releases
