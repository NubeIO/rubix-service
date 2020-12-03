# s-mon

### Running on Production

#### One time setup:
- Clone [this](https://github.com/NubeIO/common-py-libs)
- Create `venv` on inside that directory (follow instruction on [here](https://github.com/NubeIO/common-py-libs#how-to-create))

#### Commands:
```bash
sudo bash script.bash start -u=<pi|debian> -dir=<s-mon_dir> -lib_dir=<common-py-libs-dir>
sudo bash script.bash start -u=pi -dir=/home/pi/s-mon -lib_dir=/home/pi/common-py-libs
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

For `start|stop|restart` services: 

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


### Download
> POST: `/api/services/download`

> Body
```json
{
    "service": "BAC_SERVER",
    "dir": "/home/pi/bacnet-server-auto",
    "build_url": "https://api.github.com/repos/NubeDev/bacnet-flask/zipball/v1.1.3"
}
```
>Examples:
```bash
curl -X POST http://localhost:1616/api/services/download -H "Content-Type: application/json" -d '{"service":"BAC_SERVER","dir":"/home/pi/bacnet-server-auto","build_url":"https://api.github.com/repos/NubeDev/bacnet-flask/zipball/v1.1.3"}'
curl -X POST http://localhost:1616/api/services/download -H "Content-Type: application/json" -d '{"service":"WIRES","dir":"/home/pi/wires-builds-auto","build_url":"https://api.github.com/repos/NubeIO/wires-builds/zipball/v1.8.2"}'
```


### Install
> POST: `/api/services/install`

> Body
```json
{   
    "service": "BAC_SERVER",
    "dir": "/home/pi/bacnet-server-auto",
    "user": "pi",
    "lib_dir": "/home/pi/common-py-libs"
}
```
> Examples:
```bash
curl -X POST http://localhost:1616/api/services/install  -H "Content-Type: application/json" -d '{"service":"BAC_SERVER","dir":"/home/pi/bacnet-server-auto","user":"pi","lib_dir":"/home/pi/common-py-libs"}'
curl -X POST http://localhost:1616/api/services/install  -H "Content-Type: application/json" -d '{"service":"WIRES","dir":"/home/pi/wires-builds-auto","user":"pi"}'
```
