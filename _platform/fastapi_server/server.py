"""TODO"""

import importlib
from typing import Any, Optional

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator

from _platform.config.config import ServerConfig
from _platform.database.mongodb_helper import MongoDBHelper
from _platform.logger.logger import LoggerFactory


class FastAPIAppConfig(BaseModel):
    app_root: Optional[str] = ''
    version: Optional[str] = '1.0.0'
    title: Optional[str] = 'FastAPI Platform Server'
    description: Optional[str] = 'This server is an implementation of OIDC 2.0'
    modules: Optional[list[dict[str, Any]]] = None

    @validator('modules')
    @classmethod
    def set_modules(cls, modules):
        """TODO"""
        return modules or []


class FastAPIServer:
    """TODO"""

    _app = None
    _router = None
    _logger = None

    @classmethod
    async def init_module(cls, /) -> None:
        """TODO"""

        if not cls._app:
            cls._logger = LoggerFactory.get_logger('fastapi_server')

            app_config = FastAPIAppConfig.model_validate(ServerConfig.get('app'))
            
            cls._logger.info('Initializing FastAPI app ...')
            cls._app = FastAPI(
                title=app_config.title,
                description=app_config.description,
                version=app_config.version,
                # root_path=config['web_server']['app_root'],
                docs_url=f'{app_config.app_root}/docs',
                redoc_url=f'{app_config.app_root}/redoc',
                openapi_url=f'{app_config.app_root}/openapi.json',
            )

            cls._router = APIRouter(prefix=app_config.app_root)

            # modules = ['authorization.routes', 'config.routes']
            cls._logger.info('Configuring routes ...')

            for module_spec in app_config.modules:
                # print(f'importing module: {module_spec}')
                if module_spec['module_name'] == 'static_contents':
                    static_content_folder = module_spec['module_config']['static_content_folder']
                    cls._app.mount(
                        f"{cls._router.prefix}/pages",
                        StaticFiles(
                            directory=static_content_folder,
                            packages=None,
                            check_dir=True,
                            html=True,
                        ),
                        name="static",
                    )
                else:
                    pkg = importlib.import_module(module_spec['module_name'])
                    await pkg.configure_routes(cls._app, cls._router, module_spec, LoggerFactory)

            cls._app.include_router(cls._router)
            cls._logger.info('FastAPI app initialization completed.')

    @classmethod
    def get_app(cls) -> FastAPI:
        """TODO"""
        return cls._app
