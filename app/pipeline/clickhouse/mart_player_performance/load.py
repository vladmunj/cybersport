from services.clickhouse import ClickHouseClient
from app.config import CLICKHOUSE_DB

TABLE = f"{CLICKHOUSE_DB}.mart_player_performance"
COLUMNS = [
    "match_id",
    "match_date",
    "event_id",
    "event_name",
    "team_id",
    "team_name",
    "player_id",
    "nickname",
    "rating",
]

def get_existing_keys(
    client: ClickHouseClient,
    rows: list[dict],
) -> set[tuple]:
    if not rows: return set()
    match_ids = sorted({
        row["match_id"]
        for row in rows
    })
    player_ids = sorted({
        row["player_id"]
        for row in rows
    })
    team_ids = sorted({
        row["team_id"]
        for row in rows
    })
    result = client.query(
        f"""
        SELECT
            match_id,
            team_id,
            player_id
        FROM {TABLE}
        WHERE match_id IN {{match_ids:Array(UInt64)}}
          AND team_id IN {{team_ids:Array(UInt64)}}
          AND player_id IN {{player_ids:Array(UInt64)}}
        """,
        parameters={
            "match_ids": match_ids,
            "team_ids": team_ids,
            "player_ids": player_ids,
        },
    )
    return {
        (row[0], row[1], row[2])
        for row in result.result_rows
    }

def load_to_clickhouse(rows: list[dict]) -> None:
    if not rows:
        print(
            "No transformed rows found. "
            "Nothing to load."
        )
        return
    client = ClickHouseClient()
    try:
        existing_keys = get_existing_keys(
            client,
            rows,
        )
        rows_to_insert = [
            [
                row[column]
                for column in COLUMNS
            ]
            for row in rows
            if (
                row["match_id"],
                row["team_id"],
                row["player_id"],
            ) not in existing_keys
        ]
        if not rows_to_insert:
            print(
                "mart_player_performance "
                "is already up to date."
            )
            return
        client.insert(
            TABLE,
            rows_to_insert,
            column_names=COLUMNS,
        )
        print(
            f"Loaded {len(rows_to_insert)} rows "
            "into mart_player_performance."
        )
    finally:
        client.close()
