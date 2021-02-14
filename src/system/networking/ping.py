from subprocess import Popen, DEVNULL
import os
import socket


def network_ping_range(address: str, start: int, finish: int, timeout_seconds: int) -> dict:
    host_alive = []
    host_dead = []
    host_error = []
    start = start
    finish = finish
    finish += 1
    p = {}  # ip -> process
    for n in range(start, finish):  # start ping processes
        ip = address + ".%d" % n
        p[ip] = Popen(['ping', '-n', "-W", str(timeout_seconds), '-c3', ip], stdout=DEVNULL)
    while p:
        for ip, proc in p.items():
            if proc.poll() is not None:  # ping finished
                del p[ip]  # remove from the process list
                if proc.returncode == 0:
                    host_alive.append({"ip": ip, "status": True})
                elif proc.returncode == 1:
                    host_dead.append({"ip": ip, "status": False})
                else:
                    host_error.append({"ip": ip, "status": False})
                break
    return {"host_alive": host_alive, "host_dead": host_dead, "host_error": host_error}


def port_check_udp(host: str, port: int):
    try:
        res = os.system("nc -vnzu " + str(host) + " " + str(port) + " > /dev/null 2>&1")
        if res == 0:
            return True
        else:
            return False
    except:
        return False


def port_check_tcp(host: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False
