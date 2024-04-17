import clickhouse_driver


def generate_fake_data(conn, table_name, count_data):
    with conn.cursor() as cursor:
        insert_data = f"INSERT INTO {table_name} (id, user_id, view_time, event_time) VALUES"

        for i in range(1, count_data + 1):
            id = "rand()"
            user_id = "rand()"
            view_time = "rand()"
            event_time = "today()"
            insert_data += f"({id}, {user_id}, {view_time}, {event_time}),"

            if i % 10000 == 0:
                insert_data = insert_data[:-1]
                cursor.execute(insert_data)
                insert_data = (
                    f"INSERT INTO {table_name} (id, user_id, view_time, event_time) VALUES"
                )

        conn.commit()


if __name__ == "__main__":
    conn = clickhouse_driver.connect(host='localhost', database='default')
    cursor = conn.cursor()
    generate_fake_data(conn, 'test', 10000000)
    cursor.execute("SELECT COUNT(*) FROM test")
    count = cursor.fetchone()[0]
    print(f'Total rows in the table: {count}')

    conn.close()
