from clickhouse_driver import Client


class Clickhouse:
    def __init__(self, client: Client) -> None:
        self.client = client

    def init_database(self):
        self.client.execute(
            'CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER company_cluster')
        self._create_quality_table()

    def _create_quality_table(self):
        self.client.execute(
            '''
            CREATE TABLE IF NOT EXISTS ugc.quality ON CLUSTER company_cluster
                (
                    film_id UUID,
                    quality Int32,
                    event_timestamp DateTime64(6, 'Asia/Istanbul'),
                    user_id UUID,
                    produce_timestamp DateTime64(6, 'Asia/Istanbul'),
                )
                Engine=MergeTree()
            ORDER BY produce_timestamp
            '''
        )

    def insert(self, events: dict):
        for table_name, events in events.items():
            fields = events[0].dict().keys()
            values_count = ", ".join(["'%s'"] * len(fields))
            bind_values = ', '.join(f'({values_count})' % tuple(
                event.dict().values()) for event in events)
            column_names = ', '.join(fields)
            self.client.execute(
                f'INSERT INTO ugc.{table_name} ({column_names}) VALUES {bind_values}')
