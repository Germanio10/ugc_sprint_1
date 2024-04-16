from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING

from fastapi import Depends
from core.config import settings


from producers.abstract_producer import AbstractSortProducer
from typing import List, Type, TypeVar
MONGODB_URL = "mongodb://localhost:27017"

# Создаем экземпляр клиента MongoDB
mongo: AsyncIOMotorClient = AsyncIOMotorClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
T = TypeVar("T")

class MongoProducer(AbstractSortProducer):

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        self.db = self.client['UGC']

    async def get(self, collection: str, user_id: str, model: Type[T]) -> List[T]:
        query = {"user_id": user_id}
        
        documents = []
        async for document in self.db[collection].find(query):
            obj = model(**document)
            documents.append(obj)
        return documents
    
    async def get_sorted(self, collection: str, model: Type[T], field: str, ascending: bool = True) -> List[T]:
        sort_order = ASCENDING if ascending else DESCENDING
        
        documents = []
        async for document in self.db[collection].find().sort(field, sort_order):
            obj = model(**document)
            documents.append(obj)
        return documents


@lru_cache()
def get_mongo_producer(
) -> AbstractSortProducer:
    return MongoProducer()
