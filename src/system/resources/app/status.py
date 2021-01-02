from flask_restful import Resource

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp
from src.system.utils.file import get_extracted_dir
from src.system.utils.shell import systemctl_status


class StatusResource(Resource):
    def get(self):
        installed_apps = []
        for installable_app in inheritors(InstallableApp):
            dummy_app = installable_app()
            version = get_extracted_dir(dummy_app.get_installation_dir())
            if version:
                status = systemctl_status(dummy_app.service_file_name())
                installed_apps.append({'version': version.split("/")[-1], **status})
        return installed_apps
