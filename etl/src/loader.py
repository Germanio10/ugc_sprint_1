from clickhouse_client import Clickhouse


class Loader:
    def __init__(self, clickhouse: Clickhouse) -> None:
        self.clickhouse = clickhouse

    def load(self, events: dict):
        self.clickhouse.insert(events)
