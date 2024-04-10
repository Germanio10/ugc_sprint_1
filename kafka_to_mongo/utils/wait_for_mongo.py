import os

import backoff
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

load_dotenv()


@backoff.on_exception(backoff.expo, ConfigurationError)
def connect_mongo(host, port):
    print("Ожидание mongo...")
    client = MongoClient(host=host, port=port)
    yield client


if __name__ == "__main__":
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    connect_mongo(host, port)

