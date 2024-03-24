import random
from datetime import datetime

import vertica_python


def create_table(conn):
    with conn.cursor() as cursor:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test (
            id INT,
            user_id INT,
            view_time INT,
            event_time TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        conn.commit()


def generate_fake_data(conn, table_name, num_rows):
    with conn.cursor() as cursor:
        insert_statement = f"INSERT INTO {table_name} (id, user_id, view_time, event_time) VALUES (%s, %s, %s, %s)"

        batch_size = 10000
        rows = []
        for i in range(1, num_rows + 1):
            user_id = random.randint(1, 4294967295)
            view_time = random.randint(1, 4294967295)
            event_time = datetime.now()

            rows.append((i, user_id, view_time, event_time))

            if i % batch_size == 0:
                cursor.executemany(insert_statement, rows)
                rows = []

        if rows:
            cursor.executemany(insert_statement, rows)

        conn.commit()


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

    generate_fake_data(conn, "test", 10000000)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM test")
    count = cursor.fetchone()[0]
    print(f"Total rows in the table: {count}")

    conn.close()