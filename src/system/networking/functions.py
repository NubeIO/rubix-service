import netifaces
from src.system.utils.shell import command


def get_all_interfaces():
    ifaces = netifaces.interfaces()
    ifaces_gateway = {}
    gateways = netifaces.gateways()
    interfaces = {}
    gateways = gateways.get(netifaces.AF_INET, [])
    for gateway in gateways:
        ifaces_gateway[gateway[1]] = gateway[0]
    gateways_dict = dict(map(lambda gw: (gw[1], gw[0]), gateways))
    for iface in ifaces:
        if iface not in gateways_dict.keys():
            continue
        addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
        macs = netifaces.ifaddresses(iface)[netifaces.AF_LINK]
        addrs = addrs[0]
        macs = macs[0]
        address = addrs.get('addr')
        broadcast = addrs.get('broadcast')
        netmask = addrs.get('netmask')
        mac = macs.get('addr')
        cmd = f"if ip -6 addr show {iface}  | grep -q dynamic; then echo 'dhcp'; else echo 'static'; fi"
        interface_usage = command(cmd).strip('\n')
        interfaces[iface] = {
            'interface': iface,
            'interface_usage': interface_usage,
            'address': address,
            'broadcast': broadcast,
            'netmask': netmask,
            'gateway': ifaces_gateway.get(iface),
            'mac': mac
        }
    return interfaces
