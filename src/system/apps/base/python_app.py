import json
from abc import ABC

import requests

from src.system.apps.base.installable_app import InstallableApp


class PythonApp(InstallableApp, ABC):
    def get_download_link(self) -> str:
        resp = requests.get(self.get_releases_link())
        data = json.loads(resp.content)
        for row in data:
            for asset in row.get('assets', []):
                if 'armv7' in asset.get('browser_download_url'):
                    return asset.get('browser_download_url')
        return ""
