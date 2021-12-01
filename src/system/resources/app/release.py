import json
from distutils.util import strtobool

import requests
from flask import request
from packaging import version
from rubix_http.exceptions.exception import NotFoundException, PreConditionException, BadDataException
from rubix_http.resource import RubixResource

from src.system.resources.app.utils import get_app_from_service, get_github_token

OPEN_VPN_CLIENT = "OPEN_VPN_CLIENT"


class ReleaseResource(RubixResource):
    @classmethod
    def get(cls, service):
        if service == OPEN_VPN_CLIENT:
            return ["v0.0.0"]
        token: str = get_github_token()
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        app = get_app_from_service(service)
        resp = requests.get(app.get_releases_link(), headers=headers)
        data = json.loads(resp.content)
        releases = []
        try:
            all_releases: bool = False
            if 'all' in request.args:
                all_releases = bool(strtobool(request.args['all']))
        except Exception:
            raise BadDataException('Invalid query string')

        for row in data:
            if isinstance(row, str):
                raise PreConditionException(data)
            if all_releases:
                releases.append(row.get('tag_name'))
            elif version.parse(app.min_support_version) <= version.parse(row.get('tag_name')):
                releases.append(row.get('tag_name'))
        if not releases:
            raise NotFoundException(f'No version found, check your repo with version >= {app.min_support_version}')
        return releases
