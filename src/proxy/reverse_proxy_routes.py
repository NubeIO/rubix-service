import json
from typing import Union

import requests
from flask import request, Response, Blueprint, current_app
from flask_restful import abort
from mrb.message import HttpMethod
from registry.models.model_bios_info import BiosInfoModel
from registry.resources.resource_bios_info import get_bios_info
from requests.exceptions import ConnectionError

from src import AppSetting
from src.inheritors import get_instance
from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.service.utils import get_reboot_job
from src.token import get_internal_token

bp_reverse_proxy = Blueprint("reverse_proxy", __name__, url_prefix='/')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

BIOS_SERVICE_URL = 'api/service?'


@bp_reverse_proxy.route("/<path:_>", methods=methods)
def reverse_proxy_handler(_):
    url_parts = request.full_path.split("/")
    url_prefixes = {}
    settings = current_app.config[AppSetting.FLASK_KEY]
    app_settings = settings.installable_app_settings
    for app_setting in app_settings:
        dummy_app = get_instance(InstallableApp, app_setting.app_type)
        if dummy_app is not None:
            dummy_app.set_app_settings(app_setting)
            if dummy_app.gateway_access:
                url_prefixes[dummy_app.url_prefix] = dummy_app
    requested_url_prefix = url_parts[1] if len(url_parts) > 1 else ''
    port: int = get_bios_port()
    is_openvpn: bool = requested_url_prefix == 'ov' and settings.openvpn_setting.enabled
    if requested_url_prefix in url_prefixes.keys():
        app_to_redirect = url_prefixes[requested_url_prefix]
        port: int = app_to_redirect.port
    elif not (requested_url_prefix == 'bios' or is_openvpn):
        abort(404)
    del url_parts[0]
    del url_parts[0]
    path: str = "/".join(url_parts)
    actual_url: str = f'http://0.0.0.0:{port}/{path}'
    if is_openvpn:
        actual_url: str = f'http://{settings.openvpn_setting.host}:{settings.openvpn_setting.port}/{path}'
    setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    internal_token: str = get_internal_token(setting)
    try:
        resp = requests.request(request.method, actual_url, json=request.get_json(),
                                headers={**request.headers, 'Authorization': f"Internal {internal_token}"})
        # we are not upgrading BIOS, and we are changing data on the middleware (not so cool)
        if path.startswith(BIOS_SERVICE_URL) and HttpMethod[request.method.upper()] == HttpMethod.GET:
            reboot_job = get_reboot_job()
            bios_service = json.loads(resp.content)
            bios_service = {**bios_service, 'reboot_job': {
                'timer': reboot_job.get('timer', 0),
                'error': reboot_job.get('error', '')
            }}
            response = Response(json.dumps(bios_service, indent=4), resp.status_code, resp.raw.headers.items())
        else:
            response = Response(resp.content, resp.status_code, resp.raw.headers.items())
        return response
    except ConnectionError:
        abort(404)


bios_info_model: Union[BiosInfoModel, None] = get_bios_info()


def get_bios_port() -> int:
    return bios_info_model.port if bios_info_model else 1615
