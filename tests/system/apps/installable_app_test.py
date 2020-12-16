from src.system.apps.base.installable_app import InstallableApp

if __name__ == "__main__":
    app = InstallableApp.get_app('WIRES', 'v1.0.0')
    print(app.get_installation_dir())
    app = InstallableApp.get_app('BACNET_SERVER', 'v1.0.0')
    print(app.get_installation_dir())
