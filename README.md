# rubix-service

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```bash
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-service --clean --onefile \
        --add-data VERSION:. \
        --add-data systemd:systemd
    ```

  The output is: `dist/rubix-service`

## Docker build

### Build

```bash
./docker.sh
```

The output image is: `rubix-service:dev`

### Run

```bash
docker create volume rubix-service-data
docker run --rm -it -p 1616:1616 -p 1313:1313 -v rubix-service-data:/data --name rubix-service rubix-service:dev
```

## Deploy on Production

- Download release artifact
- Review help and start
```bash
Usage: run.py [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1616]
  -r, --root-dir PATH             Root dir
  -g, --global-dir PATH           Global dir
  -d, --data-dir PATH             Application data dir
  -c, --config-dir PATH           Application config dir
  -a, --artifact-dir PATH         Artifact downloaded dir
  -b, --backup-dir PATH           Backup dir
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix-Service: setting json file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  --gunicorn-config TEXT          Gunicorn: config file(gunicorn.conf.py)
  --log-level [FATAL|ERROR|WARN|INFO|DEBUG]
                                  Logging level
  --device-type [amd64|arm64|armv7]
                                  Device type  [default: armv7]
  --auth                          Enable JWT authentication.
  -l, --logging-conf TEXT         Rubix-Service: logging config file
  -h, --help                      Show this message and exit.
```

### How To Install:

Install through [rubix-bios](https://github.com/NubeIO/rubix-bios)


##### Edit config.json

- Copy config details to location: `/data/rubix-service/config/config.json` and restart service


##### Postman collection is [here](https://www.getpostman.com/collections/9e18cddf568f0a57fbaa)