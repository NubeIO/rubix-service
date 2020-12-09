from flask_restful import Api

from src import app
from src.platform.resource_wires_plat import WiresPlatResource
from src.system.networking.network_info import NetworkInfo
from src.system.resources.host_info import GetSystemMem, GetSystemTime, GetSystemDiscUsage
from src.system.resources.ping import Ping
from src.system.resources.systemctl_services import SystemctlStatus, SystemctlCommand, SystemctlStatusBool
from src.system.resources.updater import DownloadService, InstallService, DeleteData, DeleteInstallation

api = Api(app)
# 1
api_prefix = 'api'
api.add_resource(Ping, "/{}/ping".format(api_prefix))

# 2
api_prefix_system = '{}/system'.format(api_prefix)
api.add_resource(GetSystemTime, "/{}/time".format(api_prefix_system))
api.add_resource(GetSystemMem, "/{}/memory".format(api_prefix_system))
api.add_resource(GetSystemDiscUsage, "/{}/disc".format(api_prefix_system))
api.add_resource(NetworkInfo, "/{}/networking".format(api_prefix_system))

api.add_resource(SystemctlCommand, "/{}/service".format(api_prefix_system))
api.add_resource(SystemctlStatusBool, "/{}/service/up/<string:service>".format(api_prefix_system))
api.add_resource(SystemctlStatus, "/{}/service/stats/<string:service>".format(api_prefix_system))

# 3
api_prefix_services = '{}/services'.format(api_prefix)
api.add_resource(DownloadService, "/{}/download".format(api_prefix_services))
api.add_resource(InstallService, "/{}/install".format(api_prefix_services))
api.add_resource(DeleteInstallation, "/{}/delete/installation".format(api_prefix_services))
api.add_resource(DeleteData, "/{}/delete/data".format(api_prefix_services))

# 4
wires_api_prefix = '{}/wires'.format(api_prefix)
api.add_resource(WiresPlatResource, '/{}/plat'.format(wires_api_prefix))
