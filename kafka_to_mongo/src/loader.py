from logger import logger
from pymongo.errors import DuplicateKeyError


class Loader:
    def __init__(self, db) -> None:
        self.db = db
        self.rating_collection = db['rating']
        self.rating_average_collection = db['rating_info']
        self.watchlist_collection = self.db['watchlist']
        self.reviews_collection = self.db['reviews']
        self.reviews_rating_collection = self.db['reviews_rating']

    def load(self, data: dict):
        try:
            if data.get('event_type') == 'rating':
                self.rating_collection.update_one(
                    {'film_id': data['film_id'], 'user_id': data['user_id']},
                    {'$set': data},
                    upsert=True,
                )
            elif data.get('event_type') == 'watchlist':
                self.watchlist_collection.update_one(
                    {'film_id': data['film_id'], 'user_id': data['user_id']},
                    {'$set': data},
                    upsert=True,
                )
            elif data.get('event_type') == 'reviews':
                self.reviews_collection.update_one(
                    {'film_id': data['film_id'], 'user_id': data['user_id']},
                    {'$set': data},
                    upsert=True,
                )
            elif data.get('event_type') == 'reviews_rating':
                self.reviews_rating_collection.update_one(
                    {'review_id': data['review_id'], 'user_id': data['user_id']},
                    {'$set': data},
                    upsert=True,
                )
            elif data.get('event_type') == 'watchlist_rm':
                self.watchlist_collection.delete_one(
                    {'film_id': data['film_id'], 'user_id': data['user_id']}
                )

            elif data.get('event_type') == 'rating_rm':
                self.rating_collection.delete_one(
                    {'film_id': data['film_id'], 'user_id': data['user_id']}
                )
            elif data.get('event_type') is None:
                self.rating_average_collection.update_one(
                    {'film_id': data['film_id']},
                    {'$set': {'average_rating': data['average_rating']}},
                    upsert=True,
                )
        except DuplicateKeyError:
            logger.warning('{} duplicate key')
