import json

from rubix_http.exceptions.exception import NotFoundException

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
