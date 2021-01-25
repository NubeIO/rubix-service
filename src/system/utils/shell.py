import enum
import re
import subprocess


class States(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ACTIVATING = 'activating'


def execute_command(cmd, cwd=None):
    """Run command line"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)
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
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    for line in completed.stdout.decode('utf-8').splitlines():
        if 'TRUE' in line:
            return True
    return False


def systemctl_status(service):
    p = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    status_regx = r"Active:(.*) since (.*);(.*)"
    service_status = {
        'state': States.INACTIVE.value,
        'status': False
    }

    for line in output.splitlines():
        status_search = re.search(status_regx, line)
        if status_search:
            state = status_search.group(1).strip().split(" ")[0]
            service_status['state'] = state
            service_status['status'] = (state == States.ACTIVE.value)
            service_status['date_since'] = status_search.group(2).strip()
            service_status['time_since'] = status_search.group(3).strip()

    return service_status


def systemctl_installed(service):
    """
       Return True if systemd service is installed
       example: check = systemctl_installed('mosquitto')
       """
    try:
        cmd = "systemctl list-units --full -all | grep -Fq {} && echo TRUE || echo FALSE".format(service)
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    for line in completed.stdout.decode('utf-8').splitlines():
        if 'TRUE' in line:
            return True
    return False
