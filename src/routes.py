from flask import Blueprint
from flask_restful import Api

from src.platform.resource_wires_plat import WiresPlatResource
from src.system.networking.network_info import NetworkInfo
from src.system.resources.app.delete_data import DeleteDataResource
from src.system.resources.app.download import DownloadResource
from src.system.resources.app.install import InstallResource
from src.system.resources.app.release import ReleaseResource
from src.system.resources.app.status import StatusResource
from src.system.resources.app.uninstall import UnInstallResource
from src.system.resources.host_info import GetSystemMem, GetSystemTime, GetSystemDiscUsage
from src.system.resources.ping import Ping
from src.system.resources.service.command import SystemctlCommand
from src.system.resources.service.status import SystemctlStatus
from src.system.resources.service.status_bool import SystemctlStatusBool

bp_ping = Blueprint('ping', __name__, url_prefix='/api/ping')
bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_service = Blueprint('service', __name__, url_prefix='/api/system/service')
bp_app = Blueprint('app', __name__, url_prefix='/api/services')
bp_wires = Blueprint('wires', __name__, url_prefix='/api/wires')

Api(bp_ping).add_resource(Ping, '', '/')

api_system = Api(bp_system)
api_system.add_resource(GetSystemTime, '/time')
api_system.add_resource(GetSystemMem, '/memory')
api_system.add_resource(GetSystemDiscUsage, '/disc')
api_system.add_resource(NetworkInfo, '/networking')

api_service = Api(bp_service)
api_service.add_resource(SystemctlCommand, "/control")
api_service.add_resource(SystemctlStatusBool, '/up/<string:service>')
api_service.add_resource(SystemctlStatus, '/stats/<string:service>')

# 3
api_app = Api(bp_app)
api_app.add_resource(ReleaseResource, '/releases/<string:service>')
api_app.add_resource(DownloadResource, '/download')
api_app.add_resource(InstallResource, '/install')
api_app.add_resource(UnInstallResource, '/uninstall')
api_app.add_resource(DeleteDataResource, '/delete_data')
api_app.add_resource(StatusResource, '/stats')

# 4
api_wires = Api(bp_wires)
api_wires.add_resource(WiresPlatResource, '/plat')
