import json

from flask import request
from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException, BadDataException

from src.slaves.resources.slaves_base import SlavesBase
from src.system.utils.file import write_file


class SlavesSingular(SlavesBase):

    @classmethod
    def delete(cls, global_uuid):
        slaves, slaves_file = cls.get_slaves()
        if global_uuid not in slaves:
            raise NotFoundException(f"global_uuid = {global_uuid} does not exist")
        del slaves[global_uuid]
        write_file(slaves_file, json.dumps(slaves))
        return slaves


class SlavesComment(SlavesBase):

    @classmethod
    def put(cls, global_uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('comment', type=str, required=True, store_missing=False)
        data = parser.parse_args()
        comment = data.get("comment")
        return cls.update_slave_comment(global_uuid, comment)

    @classmethod
    def delete(cls, global_uuid):
        cls.update_slave_comment(global_uuid, "")
        return '', 204


class SlavesTags(SlavesBase):

    @classmethod
    def put(cls, global_uuid):
        args = request.get_json()
        tags = args.get("tags")
        if not isinstance(tags, list):
            raise BadDataException('Invalid request')
        return cls.update_slave_tags(global_uuid, tags)

    @classmethod
    def delete(cls, global_uuid):
        cls.update_slave_tags(global_uuid, [])
        return '', 204
