from yaml import load, dump
from typing import Any



try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    from yaml import Loader, Dumper


def get_config(config_path: str, /, *, run_mode: str = 'production') -> dict[Any, Any]:
    server_config = {}
    with open("./config/config.yaml") as config_stream:
        server_config = load(config_stream, Loader=Loader)

    dev_stage_config = {}
    if run_mode == 'staging':
        with open("./config/staging.yaml") as config_stream:
            dev_stage_config = load(config_stream, Loader=Loader)

    elif run_mode == 'development':
        with open("./config/development.yaml") as config_stream:
            dev_stage_config = load(config_stream, Loader=Loader)

    server_config = merge(server_config, dev_stage_config)

    return server_config


def merge(prod_conf, dev_stage_conf, path=None):
    "merges dev_stage_conf into prod_conf"
    if path is None: path = []
    for key in dev_stage_conf:
        if key in prod_conf:
            if isinstance(prod_conf[key], dict) and isinstance(dev_stage_conf[key], dict):
                merge(prod_conf[key], dev_stage_conf[key], path + [str(key)])
            else:
                prod_conf[key] = dev_stage_conf[key]
            # elif prod_conf[key] == dev_stage_conf[key]:
            #     pass # same leaf value
            # else:
            #     raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            prod_conf[key] = dev_stage_conf[key]
    return prod_conf



if __name__ == "__main__":
    # dump(server_config, Dumper=Dumper)
    print(f'....... ')