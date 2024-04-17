import os
import uuid

import pymongo
from dotenv import load_dotenv
from pymongo.collection import Collection

from utils import get_metrics_info, read_csv

load_dotenv()


def drop_collection(*, collection: Collection):
    collection.drop()


def insert_document(*, collection: Collection, data: list[dict]):
    collection.insert_many(data)


@get_metrics_info
def insert_all_data(*, collection: Collection):
    count = 0
    print('Вставка в таблицу лайков...')
    for likes in read_csv('tables/likes.csv'):
        count += len(likes)
        insert_document(collection=collection, data=likes)
    print(f'Количество записей: {count}')


@get_metrics_info
def get_user_film_ids(*, collection: Collection):
    results = collection.find().limit(5)
    return results[0]['user_id'], results[0]['film_id']


@get_metrics_info
def get_liked_films_by_user(*, collection: Collection, user_id: str):
    condition = {'user_id': user_id, 'like_': 1}
    results = collection.find(condition)
    return list(results)


@get_metrics_info
def count_likes_by_film(*, collection: Collection, film_id: str):
    condition = {'film_id': film_id, 'like_': 1}
    results = collection.count_documents(condition)
    return results


@get_metrics_info
def avg_liked_film(*, collection: Collection, film_id: str):
    pipeline = [
        {'$match': {'film_id': film_id}},
        {'$group': {'_id': 1, 'average_likes': {'$avg': '$like_'}}}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0]['average_likes']


@get_metrics_info
def add_like(*, collection: Collection, user_id: str, film_id: str):
    result = collection.insert_one({
        'key': f'{user_id}:{film_id}',
        'user_id': user_id,
        'film_id': film_id,
        'like_': 1
    })
    result_id = result.inserted_id
    return result_id


@get_metrics_info
def get_like(*, collection: Collection, user_id: str, film_id: str):
    condition = {'user_id': user_id, 'film_id': film_id}
    results = collection.find(condition)
    return results[0]


def run():
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = int(os.getenv("MONGO_PORT"))
    
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client['someDb']

    db.likes.create_index(
        [('user_id', pymongo.TEXT), ('film_id', pymongo.TEXT)])
    insert_all_data(collection=db.likes)
    print('---------------------------------------------')

    print('Получение id пользователя, id фильма..')
    user_id, film_id = get_user_film_ids(collection=db.likes)
    print('---------------------------------------------')

    print('Получение списка фильмов, понравившихся пользователю..')
    result = get_liked_films_by_user(collection=db.likes, user_id=user_id)
    print('Результат: ', len(result))
    print('---------------------------------------------')

    print('Получение количества лайков фильма...')
    result = count_likes_by_film(collection=db.likes, film_id=film_id)
    print('Результат: ', result)
    print('---------------------------------------------')

    print('Получение рейтинга фильма...')
    result = avg_liked_film(collection=db.likes, film_id=film_id)
    print(f'Результат: {result:.2f}', )
    print('---------------------------------------------')

    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())

    print('Добавление лайка...')
    add_like(collection=db.likes, user_id=user_id, film_id=film_id)
    print('---------------------------------------------')

    print('Получение лайка...')
    get_like(collection=db.likes, user_id=user_id, film_id=film_id)
    print('---------------------------------------------')

    drop_collection(collection=db.likes)
