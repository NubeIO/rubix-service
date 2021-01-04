import requests
from flask import request, Response, Blueprint
from flask_restful import abort
from requests.exceptions import ConnectionError

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp

bp_reverse_proxy = Blueprint("reverse_proxy", __name__, url_prefix='/')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']


@bp_reverse_proxy.route("/<path:url>", methods=methods)
def reverse_proxy_handler(url):
    url_parts = url.split("/")
    url_prefixes = {}
    for installable_app in inheritors(InstallableApp):
        dummy_app = installable_app()
        if dummy_app.gateway_access:
            url_prefixes[dummy_app.url_prefix] = dummy_app
    requested_url_prefix = "/{}".format(url_parts[0])
    if requested_url_prefix not in url_prefixes.keys():
        abort(404)
    app_to_redirect = url_prefixes[requested_url_prefix]
    del url_parts[0]
    actual_url = 'http://0.0.0.0:{}/{}'.format(app_to_redirect.port(), "/".join(url_parts))
    try:
        resp = requests.request(request.method, actual_url, json=request.get_json())
        response = Response(resp.content, resp.status_code, resp.raw.headers.items())
        return response
    except ConnectionError:
        abort(404)
