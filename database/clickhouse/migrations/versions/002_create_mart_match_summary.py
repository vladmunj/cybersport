from database.clickhouse.base import Migration
from app.config import CLICKHOUSE_DB

class Migration002(Migration):
    version = '002'
    def upgrade(self, client):
        client.command(f"""
            CREATE TABLE IF NOT EXISTS
            {CLICKHOUSE_DB}.mart_match_summary
            (
                match_id UInt64,
                match_date DateTime,
                event_id UInt64,
                event_name String,
                team1 String,
                team2 String,
                score String,
                loaded_at DateTime DEFAULT now()
            )
            ENGINE = MergeTree
            PARTITION BY toYYYYMM(match_date)
            ORDER BY (
                match_date,
                event_id,
                match_id
            )
        """)

    def downgrade(self, client):
        client.command(f"""
            DROP TABLE IF EXISTS
            {CLICKHOUSE_DB}.mart_match_summary
        """)
