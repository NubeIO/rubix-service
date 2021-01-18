from flask_restful import Resource, reqparse

from src.system.resources.app.utils import get_app_from_service
from src.system.utils.file import delete_existing_folder


class DeleteDataResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, required=True)
        args = parser.parse_args()
        service = args['service'].upper()
        app = get_app_from_service(service)
        deletion = delete_existing_folder(app.get_data_dir())
        return {'service': service, 'deletion': deletion}
