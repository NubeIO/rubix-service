from flask import Blueprint
from flask_restful import Api

from src.platform.resource_wires_plat import WiresPlatResource
from src.system.networking.network import NetworkInfo, NetworkSetStaticIP, NetworkSetDHCP, NetworkPingRange, \
    NetworkCheckPort
from src.system.networking.ufw import UFWRuleList, UFWStatus, UFWEnable
from src.system.resources.app.app import AppResource
from src.system.resources.app.config import UpdateLoggingResource, UpdateConfigResource, UpdateEnvResource
from src.system.resources.app.control import ControlResource
from src.system.resources.app.delete_data import DeleteDataResource
from src.system.resources.app.download import DownloadResource
from src.system.resources.app.install import InstallResource
from src.system.resources.app.release import ReleaseResource
from src.system.resources.app.stats import AppStatsResource
from src.system.resources.app.token import TokenResource
from src.system.resources.app.uninstall import UnInstallResource
from src.system.resources.app.upload import UploadResource
from src.system.resources.host_info import GetSystemMem, GetSystemTime, GetSystemDiscUsage
from src.system.resources.host_reboot import HostReboot
from src.system.resources.host_timezone import SetSystemTimeZone
from src.system.resources.ping import Ping
from src.system.resources.service.control import ServiceControl
from src.system.resources.service.service import ServiceResource
from src.system.resources.service.stats import ServiceStats
from src.users.resource_login_users import UsersLoginResource
from src.users.resource_users import UsersResource

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_networking = Blueprint('networking', __name__, url_prefix='/api/system/networking')
bp_service = Blueprint('service', __name__, url_prefix='/api/system/service')
bp_app = Blueprint('app', __name__, url_prefix='/api/app')
bp_wires = Blueprint('wires', __name__, url_prefix='/api/wires')
bp_users = Blueprint('users', __name__, url_prefix='/api/users')

api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
api_system.add_resource(GetSystemTime, '/time')
api_system.add_resource(SetSystemTimeZone, '/time/timezone')
api_system.add_resource(GetSystemMem, '/memory')
api_system.add_resource(GetSystemDiscUsage, '/disc')
api_system.add_resource(HostReboot, '/host/restart')

api_networking = Api(bp_networking)
api_networking.add_resource(NetworkInfo, '')
api_networking.add_resource(NetworkSetStaticIP, '/static')
api_networking.add_resource(NetworkSetDHCP, '/dhcp')
api_networking.add_resource(NetworkPingRange, '/ping_range')
api_networking.add_resource(NetworkCheckPort, '/check_port')
api_networking.add_resource(UFWRuleList, '/ufw/rules')
api_networking.add_resource(UFWStatus, '/ufw/status')
api_networking.add_resource(UFWEnable, '/ufw/enable')

api_service = Api(bp_service)
api_service.add_resource(ServiceResource, '')
api_service.add_resource(ServiceStats, '/stats/<string:service>')
api_service.add_resource(ServiceControl, "/control")

# 3
api_app = Api(bp_app)
api_app.add_resource(AppResource, '')
api_app.add_resource(AppStatsResource, '/stats/<string:service>')
api_app.add_resource(ControlResource, '/control')
api_app.add_resource(TokenResource, '/token')
api_app.add_resource(ReleaseResource, '/releases/<string:service>')
api_app.add_resource(DownloadResource, '/download')
api_app.add_resource(UploadResource, '/upload')
api_app.add_resource(InstallResource, '/install')
api_app.add_resource(UnInstallResource, '/uninstall')
api_app.add_resource(DeleteDataResource, '/delete_data')
api_app.add_resource(UpdateConfigResource, '/update_config')
api_app.add_resource(UpdateLoggingResource, '/update_logging')
api_app.add_resource(UpdateEnvResource, '/update_env')

# 4
api_wires = Api(bp_wires)
api_wires.add_resource(WiresPlatResource, '/plat')

# 5
api_users = Api(bp_users)
api_users.add_resource(UsersResource, '')
api_users.add_resource(UsersLoginResource, '/login', endpoint="login")
