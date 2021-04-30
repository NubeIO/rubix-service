import requests
from flask import request, Response, Blueprint, current_app
from flask_restful import abort
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
    if requested_url_prefix not in url_prefixes.keys():
        abort(404)
    app_to_redirect = url_prefixes[requested_url_prefix]
    del url_parts[0]
    del url_parts[0]
    actual_url = 'http://0.0.0.0:{}/{}'.format(app_to_redirect.port, "/".join(url_parts))
    try:
        resp = requests.request(request.method, actual_url, json=request.get_json())
        response = Response(resp.content, resp.status_code, resp.raw.headers.items())
        return response
    except ConnectionError:
        abort(404)
