import backoff

from clickhouse_client import Clickhouse, errors


class Loader:
    def __init__(self, clickhouse: Clickhouse) -> None:
        self.clickhouse = clickhouse

    @backoff.on_exception(backoff.expo, (errors.NetworkError, errors.ServerException))
    def load(self, events: dict):
        self.clickhouse.insert(events)
