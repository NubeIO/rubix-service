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
  -d, --data-dir PATH             Application data dir
  -g, --global-dir PATH           Global data dir
  -a, --artifact-dir PATH         Artifact downloaded dir
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix-Service: setting json file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  -c, --gunicorn-config TEXT      Gunicorn: config file(gunicorn.conf.py)
  --log-level [FATAL|ERROR|WARN|INFO|DEBUG]
                                  Logging level
  --device-type [amd64|arm64|armv7]
                                  Device type  [default: armv7]
  --auth                          Enable JWT authentication.
  -h, --help                      Show this message and exit.
```

### How To Install:

Install through [rubix-bios](https://github.com/NubeIO/rubix-bios)


### Authentication

> POST: `/api/users/login`
> Body
```json
{
    "username": "<username>",
    "password": "<password>"
}
```
> Use that `access_token` on header of each request

### APIs

#### GET APIs

- For returning an uptime: `/api/system/service/stats/<service>`
- For returning a `true|false`: `/api/system/service/up/<service>`


Example is top get the status of `rubix-wires`:
```
http://0.0.0.0:1616/api/system/service/stats/wires
http://0.0.0.0:1616/api/system/service/up/wires
```


#### POST APIs

For `start | stop | restart | disable | enable` services: 

> POST: `/api/system/service/control`

> Body
```json
{
    "action": "<action>",
    "service": "<service>"
}
```

> Example:
```bash
curl -X POST http://localhost:1616/api/system/service/control -H "Content-Type: application/json" -d '{"action": "restart","service":"wires"}'
```


#### Updater APIs

##### Get Releases

> GET: `api/services/releases/<service>`

>Examples:
```bash
http://localhost:1616/api/app/releases/point_server
http://localhost:1616/api/app/releases/bacnet_server
http://localhost:1616/api/app/releases/lora_raw
http://localhost:1616/api/app/releases/wires
http://localhost:1616/api/app/releases/rubix_plat
```

##### Download

> POST: `/api/services/download`

> Body
```json
{"service": "<service>","version": "<version>"}
```

```
>Examples:
```bash
curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -d '{"service":"POINT_SERVER","version":"v1.1.3"}'
curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER","version":"v1.2.1"}'
curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -d '{"service":"LORA_RAW","version":"v1.0.0"}'
curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -d '{"service":"WIRES","version":"v1.8.7"}'
curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT","version":"v1.1.5"}'
```

##### Install

> POST: `/api/services/install`

> Body
```json
{"service": "<service>","version": "<version>"}
```

> Examples:
```bash
curl -X POST http://localhost:1616/api/app/install  -H "Content-Type: application/json" -d '{"service":"POINT_SERVER","version":"v1.1.3"}'
curl -X POST http://localhost:1616/api/app/install  -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER","version":"v1.2.1"}'
curl -X POST http://localhost:1616/api/app/install  -H "Content-Type: application/json" -d '{"service":"LORA_RAW","version":"v1.0.0"}'
curl -X POST http://localhost:1616/api/app/install  -H "Content-Type: application/json" -d '{"service":"WIRES","version":"v1.8.7"}'
curl -X POST http://localhost:1616/api/app/install  -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT","version":"v1.1.5"}'
```

##### Uninstall

> POST: `/api/services/uninstall`

> Body
```json
{"service": "<service>"}
```

> Examples:
```bash
curl -X POST http://localhost:1616/api/app/uninstall  -H "Content-Type: application/json" -d '{"service":"POINT_SERVER"}'
curl -X POST http://localhost:1616/api/app/uninstall  -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER"}'
curl -X POST http://localhost:1616/api/app/uninstall  -H "Content-Type: application/json" -d '{"service":"LORA_RAW"}'
curl -X POST http://localhost:1616/api/app/uninstall  -H "Content-Type: application/json" -d '{"service":"WIRES"}'
curl -X POST http://localhost:1616/api/app/uninstall  -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT"}'
```

##### Delete Data

> POST: `/api/services/delete_data`

> Body
```json
{"service": "<service>"}
```

> Examples:
```bash
curl -X POST http://localhost:1616/api/app/delete_data  -H "Content-Type: application/json" -d '{"service":"POINT_SERVER"}'
curl -X POST http://localhost:1616/api/app/delete_data  -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER"}'
curl -X POST http://localhost:1616/api/app/delete_data  -H "Content-Type: application/json" -d '{"service":"LORA_RAW"}'
curl -X POST http://localhost:1616/api/app/delete_data  -H "Content-Type: application/json" -d '{"service":"WIRES"}'
curl -X POST http://localhost:1616/api/app/delete_data  -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT"}'
```

##### Edit config.json

- Copy config details to location: `/data/<data_dir>/config.json` and restart service
