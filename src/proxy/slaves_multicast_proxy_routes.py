import json
from typing import List

from flask import request, Blueprint, Response
from mrb.brige import MqttRestBridge
from mrb.mapper import api_to_slaves_multicast_topic_mapper
from mrb.message import Response as MessageResponse, HttpMethod

from src.discover.remote_device_registry import RemoteDeviceRegistry

bp_slaves_multicast_proxy = Blueprint("slaves_multicast_proxy", __name__, url_prefix='/slaves/multicast')
methods = ['GET']


@bp_slaves_multicast_proxy.route("/<path:_>", methods=methods)
def slaves_proxy_handler(_):
    url_parts = request.full_path.split("/")
    del url_parts[0]
    del url_parts[0]
    del url_parts[0]
    url = "/".join(url_parts)
    if request.args.get("slave_devices", None):
        available_inserted_devices_global_uuids: List[str] = request.args['slave_devices'].split(",")
    else:
        available_inserted_devices_global_uuids: List[
            str] = RemoteDeviceRegistry().available_inserted_devices_global_uuids
    timeout: str = request.args.get('timeout')
    numeric_timeout: int = int(timeout) if timeout and timeout.isnumeric() else MqttRestBridge().mqtt_setting.timeout
    if available_inserted_devices_global_uuids:
        response: MessageResponse = api_to_slaves_multicast_topic_mapper(
            slaves_global_uuids=available_inserted_devices_global_uuids,
            api=url,
            body=request.get_json(),
            http_method=HttpMethod[request.method.upper()],
            timeout=numeric_timeout
        )
        if response.error:
            return Response(json.dumps({'message': response.error_message}), response.status_code, response.headers)
        else:
            return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)
    return {"message": "Registered devices are not available or haven't registered yet!"}, 404
