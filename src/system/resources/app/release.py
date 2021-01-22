import json

import requests
from flask import current_app
from flask_restful import Resource
from packaging import version

from src import AppSetting
from src.system.resources.app.utils import get_app_from_service


class ReleaseResource(Resource):
    @classmethod
    def get(cls, service):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        token: str = app_setting.token
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        service = service.upper()
        app = get_app_from_service(service)
        resp = requests.get(app.get_releases_link(), headers=headers)
        data = json.loads(resp.content)
        releases = []
        for row in data:
            if version.parse(app.min_support_version) <= version.parse(row.get('tag_name')):
                releases.append(row.get('tag_name'))
        if not releases:
            raise ModuleNotFoundError(
                f'No version found, check your token & repo with version >= {app.min_support_version}')
        return releases
