"""TODO"""
import asyncio
import pprint
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

pp = pprint.PrettyPrinter(indent=4)


DB_CONNECTION_CONFIG = {
    "minPoolSize": 10,
    "maxPoolSize": 10,
    "w": 2,
    "journal": True,
    "username": "nf_db_user",
    "password": "nf_db_pwd",
    "replicaSet": None,
}


class DBConfigModel(BaseModel):
    minPoolSize: Optional[int] = 10
    maxPoolSize: Optional[int] = 10
    w: Optional[int] = 2
    journal: Optional[bool] = True
    connect_retry_millies: Optional[int] = 5000

    host: str
    username: str
    password: str
    database: str
    replicaSet: Optional[str] = None


class DBHelper:
    _connected: bool = False
    _client: MongoClient | None = None
    _db_con_str: str | None = None
    _db_config: DBConfigModel | None = None

    def __init__(self):
        pass

    @classmethod
    async def init_module(cls, config):

        pp.pprint(config)
        cls._db_config = DBConfigModel.parse_obj(config)
        cls._db_con_str = (
            f"mongodb://{cls._db_config.host}/{cls._db_config.database}"
        )

        await cls._connect()

    @classmethod
    async def _connect(cls):
        db_config_dict = cls._db_config.dict()
        del db_config_dict['host']
        del db_config_dict['database']
        del db_config_dict['connect_retry_millies']

        cls._client = MongoClient(
            cls._db_con_str,
            **db_config_dict,
        )

        try:
            cls._client.server_info()  # force connection on a request as the
            # connect=True parameter of MongoClient seems
            # to be useless here
            print("connection to database established.")
        except ServerSelectionTimeoutError as err:
            # do whatever you need
            cls._connected = False
            cls._client = None
            print(err)

            await asyncio.sleep(cls._db_config.connect_retry_millies // 1000)
            asyncio.run(cls._connect())

async def test():
    # print(client)

    # obj_id = ObjectId('1234')
    # pp.pprint(obj_id)

    # pp.pprint(client)

    print("\n\n\n\n")
    with DBHelper._client.nf_db.list_collections() as cursor:
        for a_col in cursor:
            pp.pprint(a_col)


async def init_module(config):
    await DBHelper.init_module(config)


if __name__ == "__main__":
    config = {
        "minPoolSize": 10,
        "maxPoolSize": 10,
        "w": 2,
        "journal": True,
        "username": "nf_db_user",
        "password": "nf_db_pwd",
        "replicaSet": None,
        "host": "localhost:27017",
        "database": "nf_db",
    }

    asyncio.run(init_module(config))
    asyncio.run(test())
    # client.close()
    # client.close()
