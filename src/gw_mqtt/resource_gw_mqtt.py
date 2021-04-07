import json

from flask import Response
from flask_restful import reqparse
from mrb.mapper import api_to_slave_topic_mapper, api_to_master_topic_mapper, api_to_slaves_topic_mapper
from mrb.message import Response as MessageResponse, HttpMethod
from rubix_http.resource import RubixResource

gw_mqtt_parser = reqparse.RequestParser()
gw_mqtt_parser.add_argument('api', type=str, required=True)
gw_mqtt_parser.add_argument('body', type=dict)
gw_mqtt_parser.add_argument('http_method', type=str, default='GET')
gw_mqtt_parser.add_argument('headers', type=dict)


class GwMqttSlaveResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('slave_global_uuid', type=str, required=True)
        parser.add_argument('api', type=str, required=True)
        parser.add_argument('body', type=dict)
        parser.add_argument('http_method', type=str, default='GET')
        parser.add_argument('headers', type=dict)
        args = parser.parse_args()
        response: MessageResponse = api_to_slave_topic_mapper(slave_global_uuid=args['slave_global_uuid'],
                                                              api=args['api'],
                                                              body=args['body'],
                                                              http_method=HttpMethod[args['http_method']],
                                                              headers=args['headers'])
        return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)


class GwMqttSlavesResource(RubixResource):
    @classmethod
    def post(cls):
        args = gw_mqtt_parser.parse_args()
        response: MessageResponse = api_to_slaves_topic_mapper(api=args['api'],
                                                               body=args['body'],
                                                               http_method=HttpMethod[args['http_method']],
                                                               headers=args['headers'])
        return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)


class GwMqttMasterResource(RubixResource):
    @classmethod
    def post(cls):
        args = gw_mqtt_parser.parse_args()
        response: MessageResponse = api_to_master_topic_mapper(api=args['api'],
                                                               body=args['body'],
                                                               http_method=HttpMethod[args['http_method']],
                                                               headers=args['headers'])
        return Response(json.dumps(response.content).encode('utf-8'), response.status_code, response.headers)
