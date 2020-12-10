from src.system.apps.base.installable_app import InstallableApp

if __name__ == "__main__":
    app = InstallableApp.get_app('WIRES')
    print(app.get_domain())
    print(app.installation_dir())
    app = InstallableApp.get_app('BAC_SERVER')
    print(app.get_domain())
    print(app.installation_dir())
