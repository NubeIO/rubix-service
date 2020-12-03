from flask_restful import Api
from src import app
from src.platform.resource_wires_plat import WiresPlatResource
from src.system.networking.bbb_ip import BBB_DHCP, BBB_STAIC
from src.system.networking.network_info import NetworkInfo
from src.system.resources.host_info import GetSystemMem, GetSystemTime, GetSystemDiscUsage
from src.system.resources.ping import Ping
from src.system.resources.systemctl_services import SystemctlStatus, SystemctlCommand, SystemctlStatusBool
from src.system.resources.updater import DownloadService, InstallService

api_prefix = 'api'
api = Api(app)

api.add_resource(GetSystemTime, "/{}/system/time".format(api_prefix))
api.add_resource(GetSystemMem, "/{}/system/memory".format(api_prefix))
api.add_resource(GetSystemDiscUsage, "/{}/system/disc".format(api_prefix))
api.add_resource(SystemctlCommand, "/{}/system/service".format(api_prefix))
api.add_resource(SystemctlStatusBool, "/{}/system/service/up/<string:service>".format(api_prefix))
api.add_resource(SystemctlStatus, "/{}/system/service/stats/<string:service>".format(api_prefix))
api.add_resource(NetworkInfo, "/{}/system/networking".format(api_prefix))
api.add_resource(BBB_DHCP, "/{}/system/networking/update/bbb/dhcp".format(api_prefix))
api.add_resource(BBB_STAIC, "/{}/system/networking/update/bbb/static".format(api_prefix))
api.add_resource(DownloadService, "/{}/services/download".format(api_prefix))
api.add_resource(InstallService, "/{}/services/install".format(api_prefix))
api.add_resource(Ping, "/{}/ping".format(api_prefix))


wires_api_prefix = f'{api_prefix}/wires'
api.add_resource(WiresPlatResource, f'/{wires_api_prefix}/plat')