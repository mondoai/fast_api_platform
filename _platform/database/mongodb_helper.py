"""TODO"""
import asyncio
import pprint
from datetime import datetime, timezone
from typing import Any, Optional, Tuple, Type

from bson.objectid import ObjectId
from bson.son import SON
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collation import Collation
from pymongo.collection import ReturnDocument
from pymongo.cursor import Cursor
from pymongo.errors import ServerSelectionTimeoutError

from _platform.config.config import ServerConfig
from _platform.logger.logger import LoggerFactory

# import ServerConfig


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
    w: Optional[int] = 1
    journal: Optional[bool] = True
    connect_retry_millies: Optional[int] = 5000

    host: str
    username: str
    password: str
    database: str
    replicaSet: Optional[str] = None


class MongoDBHelper:
    _array_fetch_limit: int = 1000
    _connected: bool = False
    _client: MongoClient | None = None
    _db_con_str: str | None = None
    _db_config: DBConfigModel | None = None
    _logger = None
    _database = None

    def __init__(self):
        pass

    @classmethod
    async def init_module(cls, /):
        """TODO"""
        cls._logger = LoggerFactory.get_logger("mongodb_helper")
        cls._db_config = DBConfigModel.parse_obj(ServerConfig.get("database:mongodb"))
        cls._db_con_str = f"mongodb://{cls._db_config.host}/{cls._db_config.database}"

        await cls._connect()

    @classmethod
    async def _connect(cls):
        db_config_dict = cls._db_config.dict()
        del db_config_dict["host"]
        del db_config_dict["database"]
        del db_config_dict["connect_retry_millies"]

        cls._client = MongoClient(
            cls._db_con_str,
            **db_config_dict,
        )

        try:
            cls._logger.info(f"connecting to: {cls._db_con_str}")
            cls._client.server_info()  # force connection on a request as the
            # connect=True parameter of MongoClient seems
            # to be useless here
            cls._logger.info("connection to database established.")
            cls._database = cls._client[cls._db_config.database]

            cls._logger.info(cls._database)
        except ServerSelectionTimeoutError as err:
            # do whatever you need
            cls._connected = False
            cls._client = None
            cls._logger.error(err)

            await asyncio.sleep(cls._db_config.connect_retry_millies // 1000)
            asyncio.run(cls._connect())

    @classmethod
    async def find(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: Optional[SON | dict | None] = None,
        limit: Optional[int | None] = None,
        projection: Optional[dict[str, int] | None] = None,
        skip: Optional[int] = 0,
        sort: Optional[list[Tuple[str, int]] | None] = None,
    ) -> Cursor:
        """TODO"""
        if not limit:
            limit = cls._array_fetch_limit
        a_coll = cls._database.get_collection(collection_name)
        if not q_filter:
            q_filter = {}
        return a_coll.find(
            filter=q_filter,
            projection=projection,
            limit=limit,
            skip=skip,
            sort=sort,
        )

    @classmethod
    async def find_one(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: Optional[SON | dict | None] = None,
        projection: Optional[dict[str, int] | None] = None,
    ) -> dict[str, Any]:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)
        if not q_filter:
            q_filter = {}
        return a_coll.find_one(filter=q_filter, projection=projection)

    @classmethod
    async def insert_one(
        cls,
        collection_name: str,
        /,
        *,
        document: dict[str, Any],
    ) -> str:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)
        document["date_created"] = datetime.now(tz=timezone.utc)
        document["date_last_updated"] = datetime.now(tz=timezone.utc)

        result = a_coll.insert_one(document=document)
        return str(result.inserted_id)

    @classmethod
    async def insert_many(
        cls,
        collection_name: str,
        /,
        *,
        documents: list[dict[str, Any]],
    ) -> list[str]:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        for document in documents:
            document["date_created"] = datetime.now(tz=timezone.utc)
            document["date_last_updated"] = datetime.now(tz=timezone.utc)

        results = a_coll.insert_many(documents=documents)
        return [str(obj_id) for obj_id in results.inserted_ids]

    @classmethod
    async def find_one_and_delete(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict,
        projection: Optional[dict[str, int] | None] = None,
        sort: Optional[list[Tuple[str, int]] | None] = None,
    ) -> dict[str, Any]:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        results = a_coll.find_one_and_delete(
            filter=q_filter,
            projection=projection,
            sort=sort,
        )

        return results

    @classmethod
    async def find_one_and_replace(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
        replacement: SON | dict[str, Any],
        projection: Optional[dict[str, int] | None] = None,
        sort: Optional[list[Tuple[str, int]] | None] = None,
        upsert: Optional[bool] = False,
        return_document: Optional[bool] = ReturnDocument.BEFORE,
    ) -> dict[Any, Any]:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        replacement["date_last_updated"] = datetime.now(tz=timezone.utc)

        results = a_coll.find_one_and_replace(
            filter=q_filter,
            replacement=replacement,
            projection=projection,
            sort=sort,
            upsert=upsert,
            return_document=return_document,
        )

        return results

    @classmethod
    async def find_one_and_update(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
        update: SON | dict[str, Any],
        projection: Optional[dict[str, int] | None] = None,
        sort: Optional[list[Tuple[str, int]] | None] = None,
        upsert: Optional[bool] = False,
        return_document: Optional[bool] = ReturnDocument.BEFORE,
    ) -> dict[Any, Any]:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        update["$set"]["date_last_updated"] = datetime.now(tz=timezone.utc)

        results = a_coll.find_one_and_update(
            filter=q_filter,
            update=update,
            projection=projection,
            sort=sort,
            upsert=upsert,
            return_document=return_document,
        )

        return results

    @classmethod
    async def count_documents(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
        limit: Optional[int | None] = None,
        skip: Optional[int] = 0,
        collation: Optional[Collation | None] = None,
    ) -> int:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)
        if limit:
            result = a_coll.count_documents(
                filter=q_filter,
                limit=limit,
                skip=skip,
                collation=collation,
            )
        else:
            result = a_coll.count_documents(
                filter=q_filter,
                skip=skip,
                collation=collation,
            )

        return result

    @classmethod
    async def distinct(
        cls,
        collection_name: str,
        /,
        *,
        key_name: str,
        q_filter: Optional[SON | dict[str, Any] | None] = None,
    ) -> list[Any]:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        results = a_coll.distinct(key=key_name, filter=q_filter)
        return results

    @classmethod
    async def delete_one(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
    ) -> int:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        results = a_coll.delete_one(filter=q_filter)
        return results.deleted_count

    @classmethod
    async def delete_many(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
    ) -> int:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        results = a_coll.delete_many(filter=q_filter)
        return results.deleted_count

    @classmethod
    async def update_one(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
        update: SON | dict[str, Any],
        upsert: Optional[bool] = False,
        bypass_document_validation: Optional[bool] = False,
    ) -> str | None:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        date_created = update.get("date_created", datetime.now(tz=timezone.utc))
        update["$set"]["date_created"] = date_created
        update["$set"]["date_last_updated"] = datetime.now(tz=timezone.utc)

        results = a_coll.update_one(
            filter=q_filter,
            update=update,
            upsert=upsert,
            bypass_document_validation=bypass_document_validation,
        )
        if results.upserted_id:
            return str(results.upserted_id)
        else:
            return None

    @classmethod
    async def update_many(
        cls,
        collection_name: str,
        /,
        *,
        q_filter: SON | dict[str, Any],
        update: SON | dict[str, Any],
        upsert: Optional[bool] = False,
        bypass_document_validation: Optional[bool] = False,
    ) -> str | None:
        """TODO"""
        a_coll = cls._database.get_collection(collection_name)

        date_created = update.get("date_created", datetime.now(tz=timezone.utc))
        update["$set"]["date_created"] = date_created
        update["$set"]["date_last_updated"] = datetime.now(tz=timezone.utc)

        results = a_coll.update_many(
            filter=q_filter,
            update=update,
            upsert=upsert,
            bypass_document_validation=bypass_document_validation,
        )
        if results.upserted_id:
            return str(results.upserted_id)
        else:
            return None


async def test():
    # print(client)

    # obj_id = ObjectId('1234')
    # pp.pprint(obj_id)

    # pp.pprint(client)
    await ServerConfig.init_module()
    await LoggerFactory.init_module()
    await MongoDBHelper.init_module()

    print("\n\n\n\n")
    with MongoDBHelper._database.list_collections() as cursor:
        for a_col in cursor:
            pp.pprint(a_col)

    print("\n\n\n\n")
    results = await MongoDBHelper.find(
        "oidc_token",
        q_filter={"_id": ObjectId("57e5a75a4d4bbaa578a210f0")},
    )
    for rec in results:
        print(rec)

    print("\n\n\n\n")
    results = await MongoDBHelper.find(
        "oidc_token",
        sort=[("date_last_updated", -1)],
    )
    print(type(results))
    for rec in results:
        print(rec)

    print("\n\n\n\n")
    results = await MongoDBHelper.find_one(
        "oidc_token",
        q_filter={"_id": ObjectId("57e5ace84d4bbaa578a210f1")},
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.insert_one(
        "test_collection",
        document={"name": "ali", "lastname": "magicland"},
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.insert_many(
        "test_collection",
        documents=[
            {"name": "ali", "lastname": "magicland"},
            {"name": "ali", "lastname": "magicland"},
            {"name": "ali", "lastname": "magicland"},
            {"name": "ali", "lastname": "magicland"},
        ],
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.find_one_and_delete(
        "test_collection",
        q_filter={"name": {"$eq": "ali"}},
        sort=[("_id", 1)],
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.find_one_and_replace(
        "test_collection",
        q_filter={"name": {"$eq": "ali"}},
        replacement={"name": "jack"},
        sort=[("_id", -1)],
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.find_one_and_update(
        "test_collection",
        q_filter={"name": {"$eq": "ali"}},
        update={
            "$set": {
                "name": "scarlet",
                "lastname": "johanson",
            },
        },
        sort=[("_id", -1)],
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.find_one_and_update(
        "test_collection",
        q_filter={"name": {"$eq": "smith"}},
        update={
            "$set": {
                "name": "hale",
                "lastname": "berry",
            },
        },
        sort=[("_id", -1)],
        upsert=True,
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.count_documents(
        "test_collection",
        q_filter={"name": {"$eq": "ali"}},
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.distinct(
        "test_collection",
        key_name="name",
        # q_filter={"name": {"$eq": "ali"}},
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.delete_one(
        "test_collection",
        q_filter={"name": {"$eq": "ali"}},
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.delete_many(
        "test_collection",
        q_filter={"name": {"$eq": "hale"}},
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.update_one(
        "test_collection",
        q_filter={"name": {"$eq": "jessica"}},
        update={
            "$set": {
                "name": "jessica jr",
                "lastname": "alba",
            },
        },
        upsert=True,
    )
    print(results)

    print("\n\n\n\n")
    results = await MongoDBHelper.update_many(
        "test_collection",
        q_filter={"name": {"$eq": "ali"}},
        update={
            "$set": {
                "name": "Dr. ali",
                # "lastname": "alba",
            },
        },
        upsert=True,
    )
    print(results)


# for testin purposes
if __name__ == "__main__":
    # asyncio.run(ServerConfig.init_module())
    asyncio.run(test())
    # client.close()
    # client.close()
