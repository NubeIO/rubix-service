import json

from flask import request, Blueprint, Response
from flask_restful import abort
from mrb.mapper import api_to_slave_topic_mapper
from mrb.message import Response as MessageResponse, HttpMethod

from src.discover.remote_device_registry import RemoteDeviceRegistry

bp_slave_proxy = Blueprint("slave_proxy", __name__, url_prefix='/slave')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']


@bp_slave_proxy.route("/<path:_>", methods=methods)
def slave_proxy_handler(_):
    url_parts = request.full_path.split("/")
    if len(url_parts) <= 3:
        abort(404)
    del url_parts[0]
    del url_parts[0]
    slave_global_uuid: str = url_parts[0]
    del url_parts[0]
    url: str = "/".join(url_parts)
    if slave_global_uuid in RemoteDeviceRegistry().available_devices_global_uuids:
        response: MessageResponse = api_to_slave_topic_mapper(slave_global_uuid=slave_global_uuid,
                                                              api=url,
                                                              body=request.get_json(),
                                                              http_method=HttpMethod[request.method.upper()])
        if response.error:
            return Response(json.dumps({'message': response.error_message}), response.status_code, response.headers)
        else:
            return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)
    return {"message": f"Slave with global_uuid {slave_global_uuid} is not active!"}, 404
