def validate_args(args: list, attrs: dict):
    if len(args) == 0 or not isinstance(args, list):
        return False
    required_attrs = {key: value for key, value in attrs.items() if attrs[key].get("required")}
    for arg in args:
        if not required_attrs.keys() <= arg.keys():
            return False
        for key, value in arg.items():
            if not isinstance(value, attrs[key].get('type')):
                return False
    return True
