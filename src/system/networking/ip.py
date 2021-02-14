import subprocess
import time
from ipaddress import IPv4Network

class dhcpcdManager:
    def __init__(self):
        self._filePath = '/etc/dhcpcd.conf'
        # self._filePath = 'src/system/networking/test.dhcpcd.conf'
        with open(self._filePath, 'r') as fp:
            self._lines = fp.readlines()

    def find_interface_line(self, interface: str) -> int:
        index = 0
        for line in self._lines:
            if line.startswith('interface ' + interface):
                return index
            index += 1
        return -1

    def find_ip_line(self, index: int) -> int:
        for line in self._lines[index:]:
            if line.startswith('static ip_address='):
                return index
            index += 1
        return -1

    def find_routers_line(self, index: int) -> int:
        for line in self._lines[index:]:
            if line.startswith('static routers='):
                return index
            index += 1
        return -1

    def find_dns_line(self, index: int) -> int:
        for line in self._lines[index:]:
            if line.startswith('static domain_name_servers='):
                return index
            index += 1
        return -1

    def set_static_info(self, interface: str, ip_address: str, routers: str, domain_name_server: str,
                        netmask: str):
        try:
            iface_index = self.find_interface_line(interface)
            netmask_number = IPv4Network(f"0.0.0.0/{netmask}").prefixlen
            if iface_index != -1:
                ip_index = self.find_ip_line(iface_index)
                routers_index = self.find_routers_line(iface_index)
                dns_index = self.find_dns_line(iface_index)
                if ip_index != -1 and routers_index != -1 and dns_index != -1:
                    self._lines[ip_index] = 'static ip_address=' + ip_address + '/' + str(netmask_number) + '\n'
                    self._lines[routers_index] = 'static routers=' + routers + '\n'
                    self._lines[dns_index] = 'static domain_name_servers=' + domain_name_server + '\n'
            else:
                if self._lines[len(self._lines) - 1] != '\n':
                    self._lines.append('\n')
                self._lines.append('interface ' + interface + '\n')
                self._lines.append('static ip_address=' + ip_address + '/' + str(netmask_number) + '\n')
                self._lines.append('static routers=' + routers + '\n')
                self._lines.append('static domain_name_servers=' + domain_name_server + '\n')

            with open(self._filePath, 'w') as fp:
                for line in self._lines:
                    fp.write(line)

            return 0
        except Exception as e:
            return e

    def remove_static_info(self, interface: str):
        try:
            iface_index = self.find_interface_line(interface)
            if iface_index == -1:
                return 1
            self._lines.pop(iface_index)
            ip_index = self.find_ip_line(iface_index)
            if ip_index != -1:
                self._lines.pop(ip_index)
            routers_index = self.find_routers_line(iface_index)
            if routers_index != -1:
                self._lines.pop(routers_index)
            dns_index = self.find_dns_line(iface_index)
            if dns_index != -1:
                self._lines.pop(dns_index)

            with open(self._filePath, 'w') as fp:
                for line in self._lines:
                    fp.write(line)

            return 0
        except Exception as e:
            return e

    def restart_interface(self,  interface: str):
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        time.sleep(1)
        subprocess.call(["sudo", "ifconfig", interface, "up"])
