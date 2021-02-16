def convert_float_decimal(f=0.0, precision=2):
    '''
        Convert a float to string of decimal.
        precision: by default 2.
        If no arg provided, return "0.00".
        '''
    return ("%." + str(precision) + "f") % f


def format_size(size, sizeIn, sizeOut, precision=0):
    '''
        Convert file/disc size to a string representing its value in B, KB, MB and GB.
        The convention is based on sizeIn as original unit and sizeOut
        as final unit.
        '''
    assert sizeIn.upper() in {"B", "KB", "MB", "GB"}, "sizeIn type error"
    assert sizeOut.upper() in {"B", "KB", "MB", "GB"}, "sizeOut type error"
    if sizeIn == "B":
        if sizeOut == "KB":
            return convert_float_decimal((size / 1024.0), precision)
        elif sizeOut == "MB":
            return convert_float_decimal((size / 1024.0 ** 2), precision)
        elif sizeOut == "GB":
            return convert_float_decimal((size / 1024.0 ** 3), precision)
    elif sizeIn == "KB":
        if sizeOut == "B":
            return convert_float_decimal((size * 1024.0), precision)
        elif sizeOut == "MB":
            return convert_float_decimal((size / 1024.0), precision)
        elif sizeOut == "GB":
            return convert_float_decimal((size / 1024.0 ** 2), precision)
    elif sizeIn == "MB":
        if sizeOut == "B":
            return convert_float_decimal((size * 1024.0 ** 2), precision)
        elif sizeOut == "KB":
            return convert_float_decimal((size * 1024.0), precision)
        elif sizeOut == "GB":
            return convert_float_decimal((size / 1024.0), precision)
    elif sizeIn == "GB":
        if sizeOut == "B":
            return convert_float_decimal((size * 1024.0 ** 3), precision)
        elif sizeOut == "KB":
            return convert_float_decimal((size * 1024.0 ** 2), precision)
        elif sizeOut == "MB":
            return convert_float_decimal((size * 1024.0), precision)


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0  # 1024 bad the size
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
