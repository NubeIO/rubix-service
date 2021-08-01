import json

import requests
from packaging import version
from rubix_http.exceptions.exception import NotFoundException, PreConditionException
from rubix_http.resource import RubixResource

from src.system.resources.app.utils import get_app_from_service, get_github_token


class ReleaseResource(RubixResource):
    @classmethod
    def get(cls, service):
        token: str = get_github_token()
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        app = get_app_from_service(service)
        resp = requests.get(app.get_releases_link(), headers=headers)
        data = json.loads(resp.content)
        releases = []
        for row in data:
            if isinstance(row, str):
                raise PreConditionException(data)
            if version.parse(app.min_support_version) <= version.parse(row.get('tag_name')):
                releases.append(row.get('tag_name'))
        if not releases:
            raise NotFoundException(f'No version found, check your repo with version >= {app.min_support_version}')
        return releases
