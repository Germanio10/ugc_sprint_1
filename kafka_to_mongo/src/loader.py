from pymongo.errors import DuplicateKeyError


class Loader:
    def __init__(self, db) -> None:
        self.db = db
        self.rating_collection = db['rating']

    def load(self, data: dict):
        try:
            if data.get('event_type') == 'rating':
                self.rating_collection.update_one({'film_id': data['film_id'], 'user_id': data['user_id']}, {'$set': data}, upsert=True)
        except DuplicateKeyError:
            print('Нельзя ставить дважды одинаковую оценку')
        if data.get('event_type') == 'rating_rm':
            self.rating_collection.delete_one({'film_id': data['film_id'], 'user_id': data['user_id']})
