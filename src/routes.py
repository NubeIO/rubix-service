from flask_restful import Api
from src import app
from src.system.resources.memory import GetSystemMem

api_prefix = 'api'
api = Api(app)


api.add_resource(GetSystemMem, f'/{api_prefix}/system/memory')
