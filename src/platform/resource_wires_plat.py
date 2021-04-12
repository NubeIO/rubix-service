import uuid
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
        data: dict = WiresPlatResource.parser.parse_args()
        wires_plat: dict = RubixRegistry().read_wires_plat()
        return cls.store_wires_plat(wires_plat, data)

    @classmethod
    def store_wires_plat_if_does_not_updated(cls):
        data: dict = {
            "client_id": "-",
            "client_name": "-",
            "site_id": "-",
            "site_name": "-",
            "device_id": cls.__create_uuid(),
            "device_name": "-",
            "site_address": "-",
            "site_city": "-",
            "site_state": "-",
            "site_zip": "-",
            "site_country": "-",
            "site_lat": "-",
            "site_lon": "-"
        }
        wires_plat: dict = RubixRegistry().read_wires_plat()
        cls.store_wires_plat(wires_plat, {**data, **wires_plat})

    @classmethod
    def store_wires_plat(cls, wires_plat: dict, data: dict):
        data['updated_on'] = datetime.utcnow().isoformat()
        if not wires_plat:
            data['global_uuid'] = cls.__create_uuid()
            data['created_on'] = data['updated_on']
        else:
            data['global_uuid'] = wires_plat.get('global_uuid') or cls.__create_uuid()
            data['created_on'] = wires_plat.get('created_on')
        return RubixRegistry().store_wires_plat(data)

    @staticmethod
    def __create_uuid() -> str:
        return str(uuid.uuid4())
