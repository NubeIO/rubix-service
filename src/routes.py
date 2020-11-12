from flask_restful import Api
from src import app
from src.system.networking.bbb_ip import BBB_DHCP, BBB_STAIC
from src.system.resources.memory import GetSystemMem
from src.system.resources.ping import Ping
from src.system.resources.systemctl_services import SystemctlStatus, SystemctlCommand, SystemctlStatusBool

api_prefix = 'api'
api = Api(app)


api.add_resource(GetSystemMem, "/{}/system/memory".format(api_prefix))
api.add_resource(SystemctlCommand, "/{}/system/service".format(api_prefix))
api.add_resource(SystemctlStatusBool, "/{}/system/service/up/<string:service>".format(api_prefix))
api.add_resource(SystemctlStatus, "/{}/system/service/stats/<string:service>".format(api_prefix))
api.add_resource(BBB_DHCP, "/{}/system/networking/update/bbb/dhcp".format(api_prefix))
api.add_resource(BBB_STAIC, "/{}/system/networking/update/bbb/static".format(api_prefix))
api.add_resource(Ping, f'/{api_prefix}/ping')
