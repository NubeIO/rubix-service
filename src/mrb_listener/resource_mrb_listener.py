from flask import current_app
from flask_restful import reqparse, marshal_with
from rubix_http.resource import RubixResource

from src import AppSetting
from src.mrb_listener.schema_mrb_listener import mrb_listener_all_fields, mrb_listener_all_attributes


class MRBListenerResource(RubixResource):
    parser = reqparse.RequestParser()
    for attr in mrb_listener_all_attributes:
        parser.add_argument(attr,
                            type=mrb_listener_all_attributes[attr]['type'],
                            required=mrb_listener_all_attributes[attr].get('required', False),
                            help=mrb_listener_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(mrb_listener_all_fields)
    def get(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        return app_setting.mqtt_rest_bridge_setting.to_dict()

    @classmethod
    @marshal_with(mrb_listener_all_fields)
    def patch(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        mqtt_rest_bridge_setting: dict = app_setting.mqtt_rest_bridge_setting.to_dict()
        data: dict = cls.parser.parse_args()
        return app_setting.reload_mrb_listener({**mqtt_rest_bridge_setting, **data})
