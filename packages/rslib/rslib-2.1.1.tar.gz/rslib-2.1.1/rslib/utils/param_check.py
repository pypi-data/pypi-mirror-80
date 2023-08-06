def param_check(config, key, param, default):
    if param is None and key in config:
        param = config[key]
    if param is None:
        param = default
    return param
