from typing import Union

import requests
from flask import request, Response, Blueprint, current_app
from flask_restful import abort
from registry.models.model_bios_info import BiosInfoModel
from registry.resources.resource_bios_info import get_bios_info
from requests.exceptions import ConnectionError

from src import AppSetting
from src.inheritors import get_instance
from src.system.apps.base.installable_app import InstallableApp

bp_reverse_proxy = Blueprint("reverse_proxy", __name__, url_prefix='/')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']


@bp_reverse_proxy.route("/<path:_>", methods=methods)
def reverse_proxy_handler(_):
    url_parts = request.full_path.split("/")
    url_prefixes = {}
    app_settings = current_app.config[AppSetting.FLASK_KEY].installable_app_settings
    for app_setting in app_settings:
        dummy_app = get_instance(InstallableApp, app_setting.app_type)
        if dummy_app is not None:
            dummy_app.set_app_settings(app_setting)
            if dummy_app.gateway_access:
                url_prefixes[dummy_app.url_prefix] = dummy_app
    requested_url_prefix = url_parts[1] if len(url_parts) > 1 else ''
    port: int = get_bios_port()
    if requested_url_prefix in url_prefixes.keys():
        app_to_redirect = url_prefixes[requested_url_prefix]
        port: int = app_to_redirect.port
    elif not requested_url_prefix == 'bios':
        abort(404)
    del url_parts[0]
    del url_parts[0]
    path: str = "/".join(url_parts)
    actual_url = f'http://0.0.0.0:{port}/{path}'
    try:
        resp = requests.request(request.method, actual_url, json=request.get_json(), headers=request.headers)
        response = Response(resp.content, resp.status_code, resp.raw.headers.items())
        return response
    except ConnectionError:
        abort(404)


def get_bios_port() -> int:
    bios_info_model: Union[BiosInfoModel, None] = get_bios_info()
    return bios_info_model.port if bios_info_model.port else 1615
