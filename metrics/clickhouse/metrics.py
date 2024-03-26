import time

import clickhouse_driver

from generate_fake_data import generate_fake_data


def get_metrics_info(func):

    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        work_time = end_time - start_time
        print(f"Function: {func.__name__}")
        print(f"Working time is {work_time:.5f} seconds")

        return result
    return inner


@get_metrics_info
def insert_100_rows(conn):
    generate_fake_data(conn, 'test', 100)


@get_metrics_info
def insert_1000_rows(conn):
    generate_fake_data(conn, 'test', 1000)


@get_metrics_info
def insert_10000_rows(conn):
    generate_fake_data(conn, 'test', 10000)


@get_metrics_info
def get_users(cursor):
    cursor.execute("SELECT user_id FROM test;")
    result = cursor.fetchall()
    return result


@get_metrics_info
def get_sum_view_time(cursor):
    cursor.execute("SELECT SUM(view_time) from test")
    result = cursor.fetchone()[0]
    return result


@get_metrics_info
def get_sum_view_time_group_users(cursor):
    cursor.execute("SELECT user_id, SUM(view_time) from test GROUP BY user_id;")
    result = cursor.fetchall()
    return result


if __name__ == "__main__":
    conn = clickhouse_driver.connect(host='localhost', database='default')
    cursor = conn.cursor()
    insert_100_rows(conn)
    insert_1000_rows(conn)
    insert_10000_rows(conn)
    get_users(cursor)
    get_sum_view_time(cursor)
    get_sum_view_time_group_users(cursor)
