from typing import Any, Iterable
import clickhouse_connect
from app.config import (
    CLICKHOUSE_DB,
    CLICKHOUSE_HOST,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USER,
)

class ClickHouseClient:
    def __init__(self):
        self.client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB,
        )

    def command(self, query: str, parameters: dict[str, Any] | None = None):
        return self.client.command(
            query,
            parameters=parameters,
        )

    def query(self, query: str, parameters: dict[str, Any] | None = None):
        return self.client.query(
            query,
            parameters=parameters,
        )

    def insert(
        self,
        table: str,
        rows: Iterable[Iterable[Any]],
        column_names: list[str],
    ):
        return self.client.insert(
            table,
            list(rows),
            column_names=column_names,
        )

    def close(self):
        self.client.close()