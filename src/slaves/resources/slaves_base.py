import json
import os
from typing import Dict

from flask import current_app
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src import AppSetting
from src.system.utils.file import read_file, write_file


class SlavesBase(RubixResource):

    @classmethod
    def get_slaves(cls) -> tuple:
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        return cls.get_slaves_by_app_setting(app_setting)

    @classmethod
    def get_slaves_by_app_setting(cls, app_setting: AppSetting):
        data_dir: str = app_setting.data_dir
        slaves_file = os.path.join(data_dir, AppSetting.default_slaves_file)
        slaves: Dict[str, Dict] = json.loads(read_file(slaves_file) or "{}")
        return slaves, slaves_file

    @classmethod
    def update_slave_comment(cls, global_uuid: str, comment: str):
        slaves, slaves_file = cls.get_slaves()
        if global_uuid not in slaves:
            raise NotFoundException(f"global_uuid = {global_uuid} does not exist")
        slave = {**slaves[global_uuid], "comment": comment}
        write_file(slaves_file, json.dumps({**slaves, global_uuid: slave}))
        return {global_uuid: {**slaves[global_uuid], "comment": comment}}

    @classmethod
    def update_slave_tags(cls, global_uuid: str, tags: list):
        slaves, slaves_file = cls.get_slaves()
        if global_uuid not in slaves:
            raise NotFoundException(f"global_uuid = {global_uuid} does not exist")
        slave = {**slaves[global_uuid], "tags": tags}
        write_file(slaves_file, json.dumps({**slaves, global_uuid: slave}))
        return {global_uuid: {**slaves[global_uuid], "tags": tags}}
