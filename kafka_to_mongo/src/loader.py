from pymongo.collection import Collection


class Loader:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def load(self, data: dict):
        self.collection.update_one({'film_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6', 'user_id': '6c0d19f6-f459-431c-9509-dc08b28878b3'}, {'$set': data}, upsert=True)
        ### Уто хардкод для проверки update_one
