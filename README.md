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
    poetry run pyinstaller run.py -n rubix-service --clean --onefile
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
./rubix-service -h

Usage: rubix-service [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1616]
  -d, --data-dir PATH             Application data dir
  -g, --global-dir PATH           Global data dir
  -a, --artifact-dir PATH         Artifact downloaded dir
  --token TEXT                    Service token to download from GitHub private repository
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix-Service: setting json file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  -c, --gunicorn-config TEXT      Gunicorn: config file(gunicorn.conf.py)
  --log-level [FATAL|ERROR|WARN|INFO|DEBUG]
                                  Logging level
  --device-type [amd64|arm64|armv7]
                                  Device type  [default: armv7]
  --install                       Install rubix-service
  --uninstall                     Uninstall rubix-service
  -h, --help                      Show this message and exit.
```

### How To Install:

Please generate token from [here](https://github.com/settings/tokens) with scope `repo`

Download appropriate rubix-service file from the [GitHub Release](https://github.com/NubeIO/rubix-service/releases) and 
extract it, then run following command to start from systemd file:

- Template: `sudo ./rubix-service -p <port> -d <data_dir> -g <global_dir> -a <artifact_dir> --token <token> --device-type <device_type> --prod --install`
- To Run on BBB & Pi: `sudo ./rubix-service -p 1616 -d /data/rubix-service -g /data -a /data/rubix-service/apps --prod --install`
- To Run on BBB & Pi with valid token: `sudo ./rubix-service -p 1616 -d /data/rubix-service -g /data -a /data/rubix-service/apps --token f31a04d4424c5eef5be61fc6e30b76aa09c94e10 --prod --install`


### How To Uninstall:
- `sudo ./rubix-service --uninstall`

### APIs

#### GET APIs

- For returning an uptime: `/api/system/service/stats/<service>`
- For returning a `true|false`: `/api/system/service/up/<service>`

Options for the `<service>` are:
```
- POINT_SERVER
- BACNET_SERVER
- LORA_RAW
- WIRES
- RUBIX_PLAT
- LORAWAN = 'lorawan-server'
- MOSQUITTO = 'mosquitto.service'
- BBB = 'nubeio-wires-plat.service'  # TODO
- DRAC = 'nubeio-wires-plat.service'  # TODO
```

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

# Install on Ubuntu
```
wget https://github.com/NubeIO/rubix-service/releases/download/v1.2.6/rubix-service-1.2.6-ab671cf.amd64.zip
unzip rubix-service-1.2.6-ab671cf.amd64.zip
sudo ./rubix-service -p 1616 -d /data/rubix-service -g /data -a /data/rubix-service/apps --device-type amd64 --prod --install
curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER","version":"v1.3.5"}'
curl -X POST http://localhost:1616/api/app/install -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER","version":"v1.3.5"}'
```

##### Edit config.json

- Copy config details to location: `/data/<data_dir>/config.json` and restart service
