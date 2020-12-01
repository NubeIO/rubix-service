# s-mon

### Running on Production

#### One time setup:
- Clone [this](https://github.com/NubeIO/common-py-libs)
- Create `venv` on inside that directory (follow instruction on [here](https://github.com/NubeIO/common-py-libs#how-to-create))

#### Commands:
```bash
sudo bash script.bash start -u=<pi|debian> -dir=<s-mon_dir> -lib_dir=<common-py-libs-dir>
sudo bash script.bash -h
```

## API

### GET
`/api/system/service/stats/SERVICE_ID` # returns an uptime
`/api/system/service/up/SERVICE_ID`  # returns a true/false

example is top get the status of rubix-wires

Options for the services

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


```
http://0.0.0.0:1616/api/system/service/stats/wires
http://0.0.0.0:1616/api/system/service/up/wires
```


### POST

`action`
```
START = start a service
STOP = start a service
RESTART = restart a service
```

`service`
service to start/stop/restart

Body
```
{
    "action": "start",
    "service": "wires"
}
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


### HTTP POST download
/api/services/download

Body
```
{
    "service": "BAC_SERVER",
    "directory": "/home/aidan/code/test",
    "build_url": "https://api.github.com/repos/NubeDev/bacnet-flask/zipball/v1.1.1"
}
```

### HTTP POST install
/api/services/install
if `test_install": true` is true then this will not run the system command (This is used for testing the API)

Body
```
{   
    "service": "BAC_SERVER",
    "_dir": "/home/aidan/code/test",
     "user": "AIDAN",
    "lib_dir": "/home/aa/",
    "test_install": true
}
```