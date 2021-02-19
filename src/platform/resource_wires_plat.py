from datetime import datetime

from flask_restful import Resource, reqparse, marshal_with, abort
from registry.registry import RubixRegistry

from src.platform.schema_wires_plat import wires_plat_all_attributes, wires_plat_all_fields


class WiresPlatResource(Resource):
    parser = reqparse.RequestParser()
    for attr in wires_plat_all_attributes:
        parser.add_argument(attr,
                            type=wires_plat_all_attributes[attr]['type'],
                            required=wires_plat_all_attributes[attr].get('required', False),
                            help=wires_plat_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def get(cls):
        wires_plat: dict = RubixRegistry().read_wires_plat()
        if not wires_plat:
            abort(404, message='Wires details not found')
        return wires_plat

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def put(cls):
        data = WiresPlatResource.parser.parse_args()
        data['updated_on'] = datetime.utcnow().isoformat()
        if not RubixRegistry().read_wires_plat():
            data['created_on'] = datetime.utcnow().isoformat()
        try:
            return RubixRegistry().store_wires_plat(data)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls):
        try:
            RubixRegistry().delete_wires_plat()
        except Exception as e:
            abort(500, message=str(e))
        return '', 204
