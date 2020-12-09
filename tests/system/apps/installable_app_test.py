from src.system.apps.mapper.service_to_installable_app_mapper import service_to_installable_app_mapper

if __name__ == "__main__":
    app = service_to_installable_app_mapper('BAC-REST')
    print(app.get_domain())
