from datetime import datetime

from flask_restful import reqparse, marshal_with
from registry.registry import RubixRegistry
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.platform.schema_wires_plat import wires_plat_all_attributes, wires_plat_all_fields


class WiresPlatResource(RubixResource):
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
            raise NotFoundException('Wires details not found')
        return wires_plat

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def put(cls):
        data = WiresPlatResource.parser.parse_args()
        data['updated_on'] = datetime.utcnow().isoformat()
        if not RubixRegistry().read_wires_plat():
            data['created_on'] = datetime.utcnow().isoformat()
        return RubixRegistry().store_wires_plat(data)
