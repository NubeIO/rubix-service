# rubix-service

### Running on Production

#### One time setup:
- Clone [this](https://github.com/NubeIO/common-py-libs)
- Create `venv` on inside that directory (follow instruction on [here](https://github.com/NubeIO/common-py-libs#how-to-create))

#### Commands:

Please generate token from [here](https://github.com/settings/tokens) with scope `repo`

```bash
sudo bash script.bash start -service_name=<service_name> -u=<pi|debian> -dir=<working_dir> -lib_dir=<common-py-libs-dir> -data_dir=<data_dir> -p=<port> -t=<token>
sudo bash script.bash start -service_name=nubeio-rubix-service.service -u=pi -dir=/home/pi/rubix-service -lib_dir=/home/pi/common-py-libs -data_dir=/data/rubix-service -p=1616 -t=f31a04d4424c5eef5be61fc6e30b76aa09c94e10
sudo bash script.bash -h
```

## APIs

### GET APIs
- For returning an uptime: `/api/system/service/stats/<service>`
- For returning a `true`/`false`: `/api/system/service/up/<service>`

Options for the `<service>` are:
```
WIRES = 'nubeio-rubix-wires.service'
PLAT = 'nubeio-wires-plat.service'
LORAWAN = 'lorawan-server'
MOSQUITTO = 'mosquitto.service'
BBB = 'nubeio-wires-plat.service'  # TODO
BAC_REST = 'nubeio-wires-plat.service'  # TODO
BAC_SERVER = 'nubeio-wires-plat.service'  # TODO
DRAC = 'nubeio-wires-plat.service'  # TODO
```

Example is top get the status of rubix-wires:
```
http://0.0.0.0:1616/api/system/service/stats/wires
http://0.0.0.0:1616/api/system/service/up/wires
```


### POST APIs

For `start | stop | restart | disable | enable` services: 

> POST: `/api/system/service`

> Body
```json
{
    "action": "<action>",
    "service": "<service>"
}
```

Where `<action>` are:
- `start`: for starting a service
- `stop`: for stopping a service
- `restart`: for restarting a service
- `disable`: for disabling a service
- `enable`: for enabling a service

> Example:
```bash
curl -X POST http://localhost:1616/api/system/service -H "Content-Type: application/json" -d '{"action": "restart","service":"wires"}'
```

## Updater

```
Step 1:
WIRES-PLAT: HTTP get all releases
Step 2: 
WIRES-PLAT: POST {service: WIRES, action: stop}: S-MON RETURN 200 or 404
Have a refresh button 
WIRES-PLAT: POST {service: WIRES, action: status}: S-MON RETURN service status
Step 3: 
WIRES-PLAT: to send service: S-MON (HTTP GET service/WIRES) http://0.0.0.0:1616/api/services/download/BAC_REST
WIRES-PLAT: HTTP POST with user selected {releases}  
S-MON: delete existing, download and unzip new S-MON RETURN 200 or 404
Step 4: 
install RETURN 200 or 404
Step 5: 
WIRES-PLAT: POST {service: WIRES, action: start}: S-MON RETURN 200 or 404
Have a refresh button 
WIRES-PLAT: POST {service: WIRES, action: status}: S-MON RETURN service status
```

### Services
- POINT_SERVER
- BACNET_SERVER
- LORA_RAW
- WIRES


### Download
> POST: `/api/services/download`

> Body
```json
{
    "service": "BACNET_SERVER",
    "build_url": "https://api.github.com/repos/NubeDev/bacnet-flask/zipball/v1.1.3"
}
```
>Examples:
```bash
curl -X POST http://localhost:1616/api/services/download -H "Content-Type: application/json" -d '{"service":"POINT_SERVER","version":"v1.1.2"}'
curl -X POST http://localhost:1616/api/services/download -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER","version":"v1.1.8"}'
curl -X POST http://localhost:1616/api/services/download -H "Content-Type: application/json" -d '{"service":"WIRES","version":"v1.8.2"}'
curl -X POST http://localhost:1616/api/services/download -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT","version":"v1.1.5"}'
```


### Install
> POST: `/api/services/install`

> Body
```json
{   
    "service": "BACNET_SERVER",
    "user": "pi",
    "lib_dir": "/home/pi/common-py-libs"
}
```
> Examples:
```bash
curl -X POST http://localhost:1616/api/services/install  -H "Content-Type: application/json" -d '{"service":"POINT_SERVER","version":"v1.1.2","user":"pi","lib_dir":"/home/pi/common-py-libs"}'
curl -X POST http://localhost:1616/api/services/install  -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER","version":"v1.1.8","user":"pi","lib_dir":"/home/pi/common-py-libs"}'
curl -X POST http://localhost:1616/api/services/install  -H "Content-Type: application/json" -d '{"service":"WIRES","version":"v1.8.2","user":"pi"}'
curl -X POST http://localhost:1616/api/services/install  -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT","version":"v1.1.5","user":"pi"}'
```


### Uninstall
> POST: `/api/services/uninstall`

> Body
```json
{   
    "service": "BACNET_SERVER"
}
```
> Examples:
```bash
curl -X POST http://localhost:1616/api/services/uninstall  -H "Content-Type: application/json" -d '{"service":"POINT_SERVER"}'
curl -X POST http://localhost:1616/api/services/uninstall  -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER"}'
curl -X POST http://localhost:1616/api/services/uninstall  -H "Content-Type: application/json" -d '{"service":"WIRES"}'
curl -X POST http://localhost:1616/api/services/uninstall  -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT"}'
```


### Delete Data
> POST: `/api/services/delete_data`

> Body
```json
{   
    "service": "BACNET_SERVER"
}
```
> Examples:
```bash
curl -X POST http://localhost:1616/api/services/delete_data  -H "Content-Type: application/json" -d '{"service":"POINT_SERVER"}'
curl -X POST http://localhost:1616/api/services/delete_data  -H "Content-Type: application/json" -d '{"service":"BACNET_SERVER"}'
curl -X POST http://localhost:1616/api/services/delete_data  -H "Content-Type: application/json" -d '{"service":"WIRES"}'
curl -X POST http://localhost:1616/api/services/delete_data  -H "Content-Type: application/json" -d '{"service":"RUBIX_PLAT"}'
```