import time

import vertica_python

from generate_fake_data import generate_fake_data, create_table


def get_metrics_info(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function: {func.__name__}")
        print(f"Execution time: {execution_time:.5f} seconds")
        return result

    return inner


@get_metrics_info
def insert_100_rows(conn):
    generate_fake_data(conn, 'test', 100)


@get_metrics_info
def insert_1000_rows(conn):
    generate_fake_data(conn, "test", 1000)


@get_metrics_info
def insert_10000_rows(conn):
    generate_fake_data(conn, "test", 10000)


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
    connection_info = {
        "host": "127.0.0.1",
        "port": 5433,
        "user": "dbadmin",
        "password": "",
        "database": "docker",
        "autocommit": True,
    }
    conn = vertica_python.connect(**connection_info)

    create_table(conn)

    insert_100_rows(conn)
    insert_1000_rows(conn)
    insert_10000_rows(conn)

    cursor = conn.cursor()

    get_users(cursor)
    get_sum_view_time(cursor)
    get_sum_view_time_group_users(cursor)

    conn.close()
