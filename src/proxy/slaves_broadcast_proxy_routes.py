import json

from flask import request, Blueprint, Response
from mrb.brige import MqttRestBridge
from mrb.mapper import api_to_slaves_broadcast_topic_mapper
from mrb.message import Response as MessageResponse, HttpMethod

bp_slaves_broadcast_proxy = Blueprint("slaves_broadcast_proxy", __name__, url_prefix='/slaves/broadcast')
methods = ['GET']


@bp_slaves_broadcast_proxy.route("/<path:_>", methods=methods)
def slaves_proxy_handler(_):
    url_parts = request.full_path.split("/")
    del url_parts[0]
    del url_parts[0]
    del url_parts[0]
    url = "/".join(url_parts)
    timeout: str = request.args.get('timeout')
    numeric_timeout: int = int(timeout) if timeout and timeout.isnumeric() else MqttRestBridge().mqtt_setting.timeout
    response: MessageResponse = api_to_slaves_broadcast_topic_mapper(
        api=url,
        body=request.get_json(),
        http_method=HttpMethod[request.method.upper()],
        timeout=numeric_timeout
    )
    if response.error:
        return Response(json.dumps({'message': response.error_message}), response.status_code, response.headers)
    else:
        return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)
