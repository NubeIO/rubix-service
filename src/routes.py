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

api.add_resource(GetSystemTime, "/{api_prefix}/system/time")
api.add_resource(GetSystemMem, f"/{api_prefix}/system/memory")
api.add_resource(GetSystemDiscUsage, f"/{api_prefix}/system/disc")
api.add_resource(SystemctlCommand, f"/{api_prefix}/system/service")
api.add_resource(SystemctlStatusBool, f"/{api_prefix}/system/service/up/<string:service>")
api.add_resource(SystemctlStatus, f"/{api_prefix}/system/service/stats/<string:service>")
api.add_resource(NetworkInfo, f"/{api_prefix}/system/networking")
api.add_resource(BBB_DHCP, f"/{api_prefix}/system/networking/update/bbb/dhcp")
api.add_resource(BBB_STAIC, f"/{api_prefix}/system/networking/update/bbb/static")
api.add_resource(DownloadService, f"/{api_prefix}/services/download")
api.add_resource(InstallService, f"/{api_prefix}/services/install")
api.add_resource(Ping, f"/{api_prefix}/ping")

wires_api_prefix = f'{api_prefix}/wires'
api.add_resource(WiresPlatResource, f'/{wires_api_prefix}/plat')
