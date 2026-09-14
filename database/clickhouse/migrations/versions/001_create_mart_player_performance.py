from database.clickhouse.base import Migration

class Migration001(Migration):
    version = '001'
    def upgrade(self, client):
        client.command("""
            CREATE TABLE IF NOT EXISTS cybersport.mart_player_performance
            (
                match_id UInt64,
                match_date DateTime,

                event_id UInt64,
                event_name String,

                team_id UInt64,
                team_name String,

                player_id UInt64,
                nickname String,

                rating Float32,

                loaded_at DateTime DEFAULT now()
            )
            ENGINE = MergeTree
            PARTITION BY toYYYYMM(match_date)
            ORDER BY (
                match_date,
                event_id,
                team_id,
                player_id
            )
        """)

    def downgrade(self, client):
        client.command("""
            DROP TABLE IF EXISTS
            cybersport.mart_player_performance
        """)
