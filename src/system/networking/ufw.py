import configparser
import json
import os
import subprocess

from flask_restful import reqparse
from rubix_http.resource import RubixResource

FNULL = open(os.devnull, "w")
GETENT = "/usr/bin/getent"
UFW = "/usr/sbin/ufw"
USER_RULES = "/etc/ufw/user.rules"
UFW_CONF = "/etc/ufw/ufw.conf"


def _ufw_config():
    with open(UFW_CONF, "r") as f:
        config_string = '[UFW]\n' + f.read()

    config = configparser.ConfigParser()
    config.read_string(config_string)
    return config


def ufw_is_enabled() -> bool:
    config = _ufw_config()
    return config["UFW"]["ENABLED"] == "yes"


def enable_ufw() -> bool:
    args = [UFW, "--force", "enable"]
    try:
        subprocess.run(args, stdout=FNULL, stderr=FNULL)
    except (IOError, OSError) as e:
        return e
    return True


def disable_ufw() -> bool:
    args = [UFW, "--force", "disable"]
    try:
        subprocess.run(args, stdout=FNULL, stderr=FNULL)
    except (IOError, OSError) as e:
        return e
    return True


def get_rule_index() -> list:
    with open(USER_RULES, "r") as in_file:
        data = in_file.readlines()
    rule_num = []
    rule_list = []
    k = 0
    for i in range(len(data)):
        if "tuple" in data[i]:
            rule = data[i][14:].split()
            rule_list.append({k + 1, rule[2], rule[1], rule[5], rule[0]})
            k += 1
            rule_num.append(i)
    return rule_list


def _set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class UFWRuleList(RubixResource):
    @classmethod
    def get(cls):
        _ = get_rule_index()
        result = json.dumps(_, default=_set_default)
        return json.loads(result)


class UFWStatus(RubixResource):
    @classmethod
    def get(cls):
        return ufw_is_enabled()


class UFWEnable(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('enable',
                            type=str,
                            help='example send a `enable or disable`',
                            required=True)
        args = parser.parse_args()
        enable = str(args['enable'])
        if enable == "enable":
            return enable_ufw()
        elif enable == "disable":
            return disable_ufw()
