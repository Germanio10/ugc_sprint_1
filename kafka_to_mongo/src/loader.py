from pymongo.collection import Collection


class Loader:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def load(self, data: dict):
        self.collection.insert_one(data)
