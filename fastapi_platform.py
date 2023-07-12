"""TODO"""
import asyncio
import multiprocessing

from fastapi import FastAPI
from gunicorn.app.wsgiapp import WSGIApplication

from _platform.config.config import ServerConfig
from _platform.database.mongodb_helper import MongoDBHelper
from _platform.fastapi_server.server import FastAPIServer
from _platform.logger.logger import LoggerFactory


class WebServerApplication(WSGIApplication):
    """TODO"""

    _config = {}
    _options = {}

    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    @classmethod
    def __init_module__(cls, app_uri, options=None):
        cls.options = options or {}
        cls.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def post_fork(server, worker):
    """TODO"""
    asyncio.run(init_platform())


def get_app() -> FastAPI:
    return FastAPIServer.get_app()


async def init_platform():
    """TODO"""

    await ServerConfig.init_module()
    await LoggerFactory.init_module()
    await MongoDBHelper.init_module()
    await FastAPIServer.init_module()


async def start_server():
    """TODO"""

    options = {
        "bind": f"{ServerConfig.get('web_server:bind_address')}:{ServerConfig.get('web_server:port')}",
        "workers": (multiprocessing.cpu_count()) + 1,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "post_fork": post_fork,
    }

    WebServerApplication("fastapi_platform:get_app()", options).run()


async def main():
    """TODO"""
    await start_server()


if __name__ == "__main__":
    print("server starting ....")
    asyncio.run(main())
