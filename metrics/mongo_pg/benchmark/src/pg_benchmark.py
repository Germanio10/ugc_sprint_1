import os
import uuid

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from utils import get_metrics_info, read_csv

load_dotenv()


def clean_table(conn: psycopg2.extensions.connection):
    with conn.cursor() as cur:
        cur.execute("""TRUNCATE TABLE likes""")
        conn.commit()


def create_table(conn: psycopg2.extensions.connection):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id SERIAL PRIMARY KEY,
            key text,
            user_id uuid,
            film_id uuid,
            like_ smallint
        )
        """)
        conn.commit()


def insert_data(conn: psycopg2.extensions.connection, table_name: str,  rows: list[dict]):
    with conn.cursor() as cur:
        columns_name = tuple(rows[0].keys())

        columns_count = ", ".join(["%s"] * len(columns_name))
        bind_values = ", ".join(
            cur.mogrify(f"({columns_count})", tuple(
                like.values())).decode("utf-8")
            for like in rows
        )
        columns_name = ", ".join(columns_name)
        cur.execute(
            f"""
        INSERT INTO {table_name} ({columns_name}) values {bind_values}
        """
        )
        conn.commit()


@get_metrics_info
def insert_all_data(conn: psycopg2.extensions.connection):
    count = 0
    print('Вставка в таблицу лайков...')
    for likes in read_csv('tables/likes.csv'):
        count += len(likes)
        insert_data(conn, 'likes', likes)
    print(f'Количество записей: {count}')


@get_metrics_info
def get_user_film_ids(conn: psycopg2.extensions.connection):
    with conn.cursor() as cur:
        cur.execute(f"""SELECT user_id, film_id FROM likes LIMIT 1""")
        return cur.fetchone()


@get_metrics_info
def get_liked_films_by_user(conn: psycopg2.extensions.connection, user_id: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT film_id FROM likes where user_id = '{user_id}' AND like_ = 1""")
        return cur.fetchall()


@get_metrics_info
def count_likes_by_film(conn: psycopg2.extensions.connection, film_id: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT count(*) FROM likes where film_id = '{film_id}' AND like_ = 1""")
        return cur.fetchone()[0]


@get_metrics_info
def avg_liked_film(conn: psycopg2.extensions.connection, film_id: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT avg(like_) FROM likes where film_id = '{film_id}'""")
        return cur.fetchone()[0]


@get_metrics_info
def add_like(conn: psycopg2.extensions.connection, user_id: str, film_id: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
            INSERT INTO likes (key, user_id, film_id, like_) values ('{user_id}:{film_id}', '{user_id}', '{film_id}', 1)
            """
        )
        conn.commit()


@get_metrics_info
def get_like(conn: psycopg2.extensions.connection, user_id: str, film_id: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT * FROM likes where user_id = '{user_id}' AND film_id = '{film_id}'
            """
        )
        cur.fetchone()


def run():
    dsn = os.getenv("POSTGRES_DSN")
    with psycopg2.connect(dsn, cursor_factory=DictCursor) as conn:
        create_table(conn)

        insert_all_data(conn)
        print('---------------------------------------------')

        print('Получение id пользователя, id фильма..')
        user_id, film_id = get_user_film_ids(conn)
        print('---------------------------------------------')

        print('Получение списка фильмов, понравившихся пользователю..')
        result = get_liked_films_by_user(conn, user_id)
        print('Результат: ', len(result))
        print('---------------------------------------------')

        print('Получение количества лайков фильма...')
        result = count_likes_by_film(conn, film_id)
        print('Результат: ', result)
        print('---------------------------------------------')

        print('Получение рейтинга фильма...')
        result = avg_liked_film(conn, film_id)
        print(f'Результат: {result:.2f}', )
        print('---------------------------------------------')

        user_id = uuid.uuid4()
        films_id = uuid.uuid4()

        print('Добавление лайка...')
        add_like(conn, user_id, film_id)
        print('---------------------------------------------')

        print('Получение лайка...')
        get_like(conn, user_id, film_id)
        print('---------------------------------------------')

        clean_table(conn)
