import subprocess


def execute_command(cmd):
    """Run command line"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    return True


def systemctl_status_check(service):
    """
    Return True if systemd service is running
    example: check = systemctl_exists('mosquitto')
    """
    try:

        cmd = "systemctl is-active {} >/dev/null 2>&1 && echo TRUE || echo FALSE".format(service)
        print(1111)
        print(cmd, 1111, service)
        print(1111)
        # cmd = f'systemctl is-active {service} >/dev/null 2>&1 && echo TRUE || echo FALSE'
        # return {"status: {}  does not exist in our system".format(service)}
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    for line in completed.stdout.decode('utf-8').splitlines():
        print(222)
        print(line, 222, service)
        print(222)
        if 'TRUE' in line:
            return True
    return False
