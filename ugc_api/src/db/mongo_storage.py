import logging

from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

logger = logging.getLogger(__name__)

mongo_client:  AsyncIOMotorClient | None = None


async def create_database() -> None:
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        db = mongo_client['UGC']

        if 'likes' not in await db.list_collection_names():
            collection = db['likes']
            await collection.create_index([('film_id', 1), ('user_id', 1)], unique=True)
        if 'likes_info' not in await db.list_collection_names():
            await db.create_collection('likes_info')
        logger.info('Connected to Mongo')
    except Exception as e:
        logger.exception(f"Error connecting to MongoDB: {e}")


async def close_connection() -> None:
    global mongo_client
    if mongo_client:
        mongo_client.close()
