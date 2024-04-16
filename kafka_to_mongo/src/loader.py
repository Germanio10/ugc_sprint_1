from pymongo.errors import DuplicateKeyError


class Loader:
    def __init__(self, db) -> None:
        self.db = db
        self.rating_collection = db['rating']
        self.watchlist_collection = db['watchlist']
        self.reviews_collection = db['reviews']
        self.reviews_rating_collection = db['reviews_rating']

    def load(self, data: dict):
        # try:
        if data.get('event_type') == 'rating':
            self.rating_collection.update_one({'film_id': data['film_id'], 'user_id': data['user_id']}, {'$set': data}, upsert=True)
        elif data.get('event_type') == 'watchlist':
            self.watchlist_collection.update_one({'film_id': data['film_id'], 'user_id': data['user_id']}, {'$set': data}, upsert=True)
        elif data.get('event_type') == 'reviews':
            self.reviews_collection.update_one({'film_id': data['film_id'], 'user_id': data['user_id']}, {'$set': data}, upsert=True)
        elif data.get('event_type') == 'reviews_rating':
            self.reviews_rating_collection.update_one({'review_id': data['review_id'], 'user_id': data['user_id']}, {'$set': data}, upsert=True)
        # except DuplicateKeyError:
        #     print('Нельзя ставить дважды одинаковую оценку')
        if data.get('event_type') == 'rating_rm':
            self.rating_collection.delete_one({'film_id': data['film_id'], 'user_id': data['user_id']})
        elif data.get('event_type') == 'watchlist_rm':
            self.watchlist_collection.delete_one({'film_id': data['film_id'], 'user_id': data['user_id']})
