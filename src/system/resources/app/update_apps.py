import gevent
from flask import current_app
from flask_restful import reqparse
from rubix_http.exceptions.exception import PreConditionException
from rubix_http.resource import RubixResource

from src.system.apps.base.installable_app import InstallableApp
from src.system.resources.app.utils import get_app_from_service


class UpdateAppsResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('apps', required=True, type=dict, action='append')
        args = parser.parse_args()
        update_results = []
        threads = []
        rubix_plat = None
        rubix_plat_args = {}
        for arg in args['apps']:
            try:
                service = arg['service'].upper()
                version = arg['version']
                delete_db = bool(arg.get('delete_db'))
                delete_config = bool(arg.get('delete_config'))
                app: InstallableApp = get_app_from_service(service, version)
                app_context = current_app._get_current_object().app_context
                if service == 'RUBIX_PLAT':
                    rubix_plat = app
                    rubix_plat_args = arg
                else:
                    threads.append(gevent.spawn(app.update_app_async, delete_db, delete_config, app_context))
            except KeyError as e:
                raise PreConditionException(f'{str(e)} is missing')
        gevent.joinall(threads)
        for thread in threads:
            update_results.append(thread.value)
        if rubix_plat is not None:
            delete_db = bool(rubix_plat_args.get('delete_db'))
            delete_config = bool(rubix_plat_args.get('delete_config'))
            update_results.append(rubix_plat.update_app(delete_db, delete_config))
        return update_results
