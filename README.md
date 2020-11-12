# s-mon
#### How to run

### Installing (for linux)

```
sudo python3 -m venv venv
source venv/bin/activate
sudo pip3 install --upgrade pip
sudo pip3 install -r requirements.txt
sudo python3 run.py
```

```
sudo journalctl -f -u nubeio-s-mon.service
sudo systemctl start nubeio-s-mon.service
sudo systemctl stop nubeio-s-mon.service
sudo systemctl restart nubeio-s-mon.service
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