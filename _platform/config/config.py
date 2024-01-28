import asyncio
from os import getenv
from typing import Any, Optional

from yaml import dump, load


try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader

except ImportError:
    from yaml import Dumper, Loader


class ServerConfig:
    """TODO"""

    _server_config_dict: dict[Any, Any] = {}
    _initialized = False
    _server_config = None

    @classmethod
    async def init_module(cls, /) -> None:
        """TODO"""

        if cls._initialized:
            return

        run_mode = getenv("RUN_MODE", "production")

        print(f'\nserver running in: {run_mode=} ...\n')

        cls._server_config_dict = {}
        with open("./config/config.yaml", encoding="utf-8") as config_stream:
            cls._server_config_dict = load(config_stream, Loader=Loader)

        dev_stage_config = {}
        if run_mode == "staging":
            with open("./config/staging.yaml", encoding="utf-8") as config_stream:
                dev_stage_config = load(config_stream, Loader=Loader)

        elif run_mode == "development":

            print('in developement mode')
            with open("./config/development.yaml", encoding="utf-8") as config_stream:
                dev_stage_config = load(config_stream, Loader=Loader)

        cls._server_config_dict = merge(cls._server_config_dict, dev_stage_config)

        cls._initialized = True
        cls._server_config = ServerConfig()

    @classmethod
    def get(cls, param_path: str, /) -> Any:
        """param_path is delimited by : (colon)"""

        elem = cls._server_config_dict
        for path_elem in param_path.strip(":").split(":"):
            elem = elem.get(path_elem)

        return elem


def merge(prod_conf, dev_stage_conf, path=None):
    """merges dev_stage_conf into prod_conf"""
    if path is None:
        path = []
    for key in dev_stage_conf:
        if key in prod_conf:
            if isinstance(prod_conf[key], dict) and isinstance(
                dev_stage_conf[key], dict
            ):
                merge(prod_conf[key], dev_stage_conf[key], path + [str(key)])
            else:
                prod_conf[key] = dev_stage_conf[key]
        else:
            prod_conf[key] = dev_stage_conf[key]
    return prod_conf


if __name__ == "__main__":
    asyncio.run(ServerConfig.init_module())
    temp_var = ServerConfig.get(
        "openid_connect_fastapi:configuration:scopes_supported:"
    )

    print(temp_var)

    print()
