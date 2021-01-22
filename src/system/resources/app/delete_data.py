from flask_restful import Resource, reqparse, abort

from src.system.apps.base.frontend_app import FrontendApp
from src.system.apps.base.python_app import PythonApp
from src.system.resources.app.utils import get_app_from_service
from src.system.systemd.systemd import AppSystemd
from src.system.utils.file import delete_existing_folder, get_extracted_dir


class DeleteDataResource(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app = get_app_from_service(service)
        deletion = delete_existing_folder(app.get_data_dir())
        restart = False
        if deletion:
            if isinstance(app, PythonApp):
                systemd = AppSystemd(app.service_file_name, app.pre_start_sleep, app.get_wd(), app.port,
                                     app.get_data_dir(), app.repo_name, app.description)
                try:
                    restart = systemd.restart()
                except Exception as e:
                    abort(501, message=str(e))
            elif isinstance(app, FrontendApp):
                version = get_extracted_dir(app.get_installation_dir())
                if version:
                    app.set_version(version)
                    restart = app.execute_restart()

        return {'service': service, 'deletion': deletion, 'restart': restart}
