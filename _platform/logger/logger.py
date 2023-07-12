import logging.config
import logging

import coloredlogs

# import coloredlogs
from typing import Any
from _platform.config.config import ServerConfig


class LoggerFactory:
    """TODO"""

    __loggers = {}
    __initialized = False

    def __init__(self):
        pass

    @classmethod
    async def init_module(cls):
        """TODO"""

        if cls.__initialized:
            return

        logging.config.dictConfig(ServerConfig.get("logger"))
        coloredlogs.install(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        cls.__initialized = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """TODO"""
        if not cls.__initialized:
            raise Exception("logger factory not initialized!")

        if name in cls.__loggers.keys():
            return cls.__loggers[name]
        else:
            new_logger = logging.getLogger(name)
            cls.__loggers[name] = new_logger
            coloredlogs.install(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                logger=new_logger,
            )
            return new_logger
