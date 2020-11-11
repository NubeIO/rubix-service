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
