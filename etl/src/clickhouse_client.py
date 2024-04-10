import backoff
from clickhouse_driver import Client, errors


class Clickhouse:
    def __init__(self, client: Client) -> None:
        self.client = client

    @backoff.on_exception(backoff.expo, (errors.NetworkError, errors.ServerException))
    def init_database(self):
        self.client.execute(
            'CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER company_cluster')
        self._create_quality_table()
        self._create_film_progress_table()
        self._create_click_tracking_table()
        self._create_filter_table()
        self._create_like_table()

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

    def _create_film_progress_table(self):
        self.client.execute(
            '''
            CREATE TABLE IF NOT EXISTS ugc.progress ON CLUSTER company_cluster
                (
                    film_id UUID,
                    watching_time Int32,
                    film_percentage Int32,
                    event_timestamp DateTime64(6, 'Asia/Istanbul'),
                    user_id UUID,
                    produce_timestamp DateTime64(6, 'Asia/Istanbul')
                )
                Engine=MergeTree()
            ORDER BY produce_timestamp
            '''
        )

    def _create_click_tracking_table(self):
        self.client.execute(
            '''
            CREATE TABLE IF NOT EXISTS ugc.click_info ON CLUSTER company_cluster
                (
                    url String,
                    click_time DateTime64(6, 'Asia/Istanbul'),
                    time_on_page Int32,
                    event_timestamp DateTime64(6, 'Asia/Istanbul'),
                    user_id UUID,
                    produce_timestamp DateTime64(6, 'Asia/Istanbul')
                )
                Engine=MergeTree()
            ORDER BY produce_timestamp
            '''
        )

    def _create_filter_table(self):
        self.client.execute(
            '''
            CREATE TABLE IF NOT EXISTS ugc.filter ON CLUSTER company_cluster
                (
                    genre_id UUID,
                    genre String,
                    sort String,
                    event_timestamp DateTime64(6, 'Asia/Istanbul'),
                    user_id UUID,
                    produce_timestamp DateTime64(6, 'Asia/Istanbul')
                )
                Engine=MergeTree()
            ORDER BY produce_timestamp
            '''
        )

    def _create_like_table(self):
        self.client.execute(
            '''
            CREATE TABLE IF NOT EXISTS ugc.like ON CLUSTER company_cluster
                (
                    film_id UUID,
                    rating UInt8,
                    event_timestamp DateTime64(6, 'Asia/Istanbul'),
                    user_id UUID,
                    produce_timestamp DateTime64(6, 'Asia/Istanbul')
                )
                Engine=MergeTree()
            ORDER BY produce_timestamp
            '''
        )
    def insert(self, events: dict):
        for table_name, events in events.items():
            fields = events[0].dict().keys()
            column_names = ', '.join(fields)
            values = tuple(event.dict() for event in events)
            self.client.execute(f'INSERT INTO ugc.{table_name} ({column_names}) VALUES', values)
