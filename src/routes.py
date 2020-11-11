from flask_restful import Api
from src import app
from src.system.resources.memory import GetSystemMem
from src.system.resources.systemctl_services import SystemctlStatus

api_prefix = 'api'
api = Api(app)


api.add_resource(GetSystemMem, "/{}/system/memory".format(api_prefix))
api.add_resource(SystemctlStatus, "/{}/system/service/<string:service>".format(api_prefix))
