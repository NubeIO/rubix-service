import json

from flask import request, Blueprint, Response
from flask_restful import abort
from mrb.mapper import api_to_master_topic_mapper
from mrb.message import Response as MessageResponse, HttpMethod

bp_master_proxy = Blueprint("master_proxy", __name__, url_prefix='/master')
methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']


@bp_master_proxy.route("/<path:_>", methods=methods)
def slave_proxy_handler(_):
    url_parts = request.full_path.split("/")
    if len(url_parts) <= 2:
        abort(404)
    del url_parts[0]
    del url_parts[0]
    url: str = "/".join(url_parts)
    response: MessageResponse = api_to_master_topic_mapper(api=url,
                                                           body=request.get_json(),
                                                           http_method=HttpMethod[request.method.upper()])
    if response.error:
        return Response(json.dumps({'message': response.error_message}), response.status_code, response.headers)
    else:
        return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)
