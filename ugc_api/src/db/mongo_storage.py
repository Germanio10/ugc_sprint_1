import logging

from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

mongo_client: AsyncIOMotorClient | None = None


async def create_database() -> None:
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        db = mongo_client['UGC']

        if 'rating' not in await db.list_collection_names():
            collection = db['rating']
            await collection.create_index([('film_id', 1), ('user_id', 1)], unique=True)
        if 'rating_info' not in await db.list_collection_names():
            collection = db['rating_info']
            await collection.create_index([('film_id', 1)], unique=True)
        if 'watchlist' not in await db.list_collection_names():
            collection = db['watchlist']
            await collection.create_index([('film_id', 1), ('user_id', 1)], unique=True)
        if 'reviews' not in await db.list_collection_names():
            collection = db['reviews']
            await collection.create_index([('film_id', 1), ('user_id', 1)], unique=True)
        if 'reviews_rating' not in await db.list_collection_names():
            collection = db['reviews_rating']
            await collection.create_index([('review_id', 1), ('user_id', 1)], unique=True)

        logger.info('Connected to Mongo')
    except Exception as e:
        logger.exception(f"Error connecting to MongoDB: {e}")


async def close_connection() -> None:
    global mongo_client
    if mongo_client:
        mongo_client.close()
