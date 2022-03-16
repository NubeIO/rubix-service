from rubix_http.resource import RubixResource

from src.bios.utils import clear_bios_app_state


class ClearAppStateResource(RubixResource):
    @classmethod
    def delete(cls):
        clear_bios_app_state()
        return {'message': 'Bios app state is cleared'}
