import enum
from flask_restful import Resource, reqparse, abort
from src.system.utils.shell_commands import execute_command, systemctl_status_check

interface = 'eth0'
dhcp_static = True
ip = "body.eth1Ip;"
sub = "body.eth1Ip;"
gate = "body.eth1Ip;"
name_server = "body.eth1Ip;"



# setIP = `sudo connmanctl config ${iface} --ipv4 manual ${ipAddress} ${subnetMask} ${gateway} --nameservers 8.8.8.8 8.8.4.4`;
# setIpDHCP = `sudo connmanctl config ${iface} --ipv4 dhcp`;

