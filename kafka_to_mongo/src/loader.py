from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class Loader:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def load(self, data: dict):
        try:
            if data.get('event_type') == 'rating':
                self.collection.update_one({'film_id': data['film_id'], 'user_id': data['user_id']}, {'$set': data}, upsert=True)
        except DuplicateKeyError:
            print('Нельзя ставить дважды одинаковую оценку')
        if data.get('event_type') == 'rating_rm':
            self.collection.delete_one({'film_id': data['film_id'], 'user_id': data['user_id']})
