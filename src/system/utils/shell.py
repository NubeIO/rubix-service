import enum
import re
import subprocess


class States(enum.Enum):
    """
    Available unit active states list of systemctl, `systemctl --state=help`.
    """
    ACTIVE = 'active'
    RELOADING = 'reloading'
    INACTIVE = 'inactive'
    FAILED = 'failed'
    ACTIVATING = 'activating'
    DEACTIVATING = 'deactivating'
    MAINTENANCE = 'maintenance'


def command(cmd, _input=""):
    rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=_input.encode("utf-8"))
    assert rst.returncode == 0, rst.stderr.decode("utf-8")
    try:
        return rst.stdout.decode("utf-8")
    except ValueError:
        return "Error"


def execute_command_with_exception(cmd, cwd=None):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)


def execute_command(cmd, cwd=None) -> bool:
    """Run command line"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)
    except Exception:
        return False
    return True


def systemctl_status_check(service) -> bool:
    """
    Return True if systemd service is running
    example: check = systemctl_exists('mosquitto')
    """
    try:
        cmd = "systemctl is-active {} >/dev/null 2>&1 && echo TRUE || echo FALSE".format(service)
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except Exception:
        return False
    for line in completed.stdout.decode('utf-8').splitlines():
        if 'TRUE' in line:
            return True
    return False


def systemctl_status(service) -> dict:
    try:
        output = subprocess.run(["systemctl", "status", service], stdout=subprocess.PIPE)
    except Exception:
        return {}
    output = output.stderr.decode('utf-8')
    active_status_regx = r"Active:(.*) since (.*);(.*)"
    loaded_status_regx = f"Loaded:(.*); (.*);(.*)"
    service_status = {}
    for line in output.splitlines():
        active_status_search = re.search(active_status_regx, line)
        if active_status_search:
            state = active_status_search.group(1).strip().split(" ")[0]
            service_status['state'] = state
            service_status['status'] = (state == States.ACTIVE.value)
            service_status['date_since'] = active_status_search.group(2).strip()
            service_status['time_since'] = active_status_search.group(3).strip()
        loaded_status_search = re.search(loaded_status_regx, line)
        if loaded_status_search:
            service_status['is_enabled'] = loaded_status_search.group(2).strip() == 'enabled'
    return service_status


def systemctl_installed(service) -> bool:
    """
    Return True if systemd service is installed
    example: check = systemctl_installed('mosquitto')
    """
    try:
        cmd: str = "systemctl status {} | wc -l | grep -w -Fq 0 && echo FALSE || echo TRUE".format(service)
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except Exception:
        return False
    for line in completed.stdout.decode('utf-8').splitlines():
        if 'TRUE' in line:
            return True
    return False

