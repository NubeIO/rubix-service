from flask_restful import Api
from src import app
from src.system.resources.memory import GetSystemMem
from src.system.resources.systemctl_services import SystemctlStatus, SystemctlCommand, SystemctlStatusBool

api_prefix = 'api'
api = Api(app)


api.add_resource(GetSystemMem, "/{}/system/memory".format(api_prefix))
api.add_resource(SystemctlCommand, "/{}/system/service".format(api_prefix))
api.add_resource(SystemctlStatusBool, "/{}/system/service/up/<string:service>".format(api_prefix))
api.add_resource(SystemctlStatus, "/{}/system/service/stats/<string:service>".format(api_prefix))
