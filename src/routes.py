from flask import Blueprint
from flask_restful import Api

from src.platform.resource_wires_plat import WiresPlatResource
from src.system.networking.network_info import NetworkInfo
from src.system.resources.host_info import GetSystemMem, GetSystemTime, GetSystemDiscUsage
from src.system.resources.ping import Ping
from src.system.resources.systemctl_services import SystemctlStatus, SystemctlCommand, SystemctlStatusBool
from src.system.resources.updater import DownloadService, InstallService, DeleteData, DeleteInstallation

bp_ping = Blueprint('ping', __name__, url_prefix='/api/ping')
bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_service = Blueprint('service', __name__, url_prefix='/api/system/service')
bp_app = Blueprint('app', __name__, url_prefix='/api/services')
bp_wires = Blueprint('wires', __name__, url_prefix='/api/wires')

Api(bp_ping).add_resource(Ping, '/')

api_system = Api(bp_system)
api_system.add_resource(GetSystemTime, '/time')
api_system.add_resource(GetSystemMem, '/memory')
api_system.add_resource(GetSystemDiscUsage, '/disc')
api_system.add_resource(NetworkInfo, '/networking')

api_service = Api(bp_service)
api_service.add_resource(SystemctlCommand, "/")
api_service.add_resource(SystemctlStatusBool, '/up/<string:service>')
api_service.add_resource(SystemctlStatus, '/stats/<string:service>')

# 3
api_app = Api(bp_app)
api_app.add_resource(DownloadService, '/download')
api_app.add_resource(InstallService, '/install')
api_app.add_resource(DeleteInstallation, '/uninstall')
api_app.add_resource(DeleteData, '/delete_data')

# 4
api_wires = Api(bp_wires)
api_wires.add_resource(WiresPlatResource, '/plat')
