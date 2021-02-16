def convert_float_decimal(f=0.0, precision=2):
    """
    Convert a float to string of decimal.
    precision: by default 2.
    If no arg provided, return "0.00".
    """
    return ("%." + str(precision) + "f") % f


def format_size(size, size_in, size_out, precision=0):
    """
    Convert file/disc size to a string representing its value in B, KB, MB and GB.
    The convention is based on size_in as original unit and size_out
    as final unit.
    """
    assert size_in.upper() in {"B", "KB", "MB", "GB"}, "size_in type error"
    assert size_out.upper() in {"B", "KB", "MB", "GB"}, "size_out type error"
    if size_in == "B":
        if size_out == "KB":
            return convert_float_decimal((size / 1024.0), precision)
        elif size_out == "MB":
            return convert_float_decimal((size / 1024.0 ** 2), precision)
        elif size_out == "GB":
            return convert_float_decimal((size / 1024.0 ** 3), precision)
    elif size_in == "KB":
        if size_out == "B":
            return convert_float_decimal((size * 1024.0), precision)
        elif size_out == "MB":
            return convert_float_decimal((size / 1024.0), precision)
        elif size_out == "GB":
            return convert_float_decimal((size / 1024.0 ** 2), precision)
    elif size_in == "MB":
        if size_out == "B":
            return convert_float_decimal((size * 1024.0 ** 2), precision)
        elif size_out == "KB":
            return convert_float_decimal((size * 1024.0), precision)
        elif size_out == "GB":
            return convert_float_decimal((size / 1024.0), precision)
    elif size_in == "GB":
        if size_out == "B":
            return convert_float_decimal((size * 1024.0 ** 3), precision)
        elif size_out == "KB":
            return convert_float_decimal((size * 1024.0 ** 2), precision)
        elif size_out == "MB":
            return convert_float_decimal((size * 1024.0), precision)


def convert_bytes(num):
    """
    this function will convert bytes to MB... GB... etc
    """
    step_unit = 1000.0  # 1024 bad the size
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
