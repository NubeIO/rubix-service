from rubix_http.resource import RubixResource, NotFoundException

from src.bios.utils import clear_bios_app_state


class ClearAppStateResource(RubixResource):
    @classmethod
    def delete(cls):
        if not clear_bios_app_state():
            raise NotFoundException(f'Bios app state not found')
        return {'message': 'Bios app state is cleared'}
