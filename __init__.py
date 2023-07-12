"""TODO"""
from fastapi_platform import start_server, init_platform

from ._platform.config.config import ServerConfig
from ._platform.database.mongodb_helper import MongoDBHelper
from ._platform.logger.logger import LoggerFactory
