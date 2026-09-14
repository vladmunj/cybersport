from services.clickhouse import ClickHouseClient
from services.db import Db
from models.event import Event
from models.match import Match
from models.player import Player
from models.statistic import Statistic
from models.team import Team
from app.config import CLICKHOUSE_DB
from services.sentry import Sentry
from helpers.transform import row_to_dict

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

def _load_source_data():
    statistics = Db.query(Statistic).select([
        "match_id",
        "player_id",
        "team_id",
        "rating",
    ]).get()
    matches = Db.query(Match).select([
        "id",
        "external_id",
        "event_id",
        "date",
    ]).get()
    events = Db.query(Event).select([
        "id",
        "title",
    ]).get()
    players = Db.query(Player).select([
        "id",
        "nickname",
    ]).get()
    teams = Db.query(Team).select([
        "id",
        "name",
    ]).get()
    matches_map = {
        row.id: row
        for row in matches
    }
    events_map = {
        row.id: row
        for row in events
    }
    players_map = {
        row.id: row
        for row in players
    }
    teams_map = {
        row.id: row
        for row in teams
    }
    rows = []
    skipped_matches = []
    for statistic in statistics:
        match = matches_map.get(statistic.match_id)
        player = players_map.get(statistic.player_id)
        team = teams_map.get(statistic.team_id)
        if match is None:
            raise ValueError(f"Match not found: {statistic.match_id}")
        if player is None:
            raise ValueError(f"Player not found: {statistic.player_id}")
        if team is None:
            raise ValueError(f"Team not found: {statistic.team_id}")
        event = events_map.get(match.event_id)
        if event is None:
            raise ValueError(f"Event not found: {match.event_id}")
        if match.date is None:
            skipped_matches.append(row_to_dict(match, exclude={'date'}))
            continue
        rows.append({
            "match_id": match.id,
            "match_date": match.date,
            "event_id": event.id,
            "event_name": event.title,
            "team_id": team.id,
            "team_name": team.name,
            "player_id": player.id,
            "nickname": player.nickname,
            "rating": float(statistic.rating) if statistic.rating is not None else 0.0,
        })
    if skipped_matches:
        Sentry.warning(
            message="Match skipped: date is missing",
            extra={
                'skipped_matches_count': len(skipped_matches),
                'skipped_matches': skipped_matches,
            },
            tags={
                "pipeline": "mart_player_performance",
                "reason": "missing_match_date",
            },
        )
    return rows

def _get_existing_keys(client: ClickHouseClient, rows: list[dict]):
    if not rows: return set()
    match_ids = sorted({row["match_id"] for row in rows})
    player_ids = sorted({row["player_id"] for row in rows})
    team_ids = sorted({row["team_id"] for row in rows})
    result = client.query(
        f"""
        SELECT match_id, team_id, player_id
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


def run_mart_player_performance_pipeline():
    source_rows = _load_source_data()
    if not source_rows:
        print("No statistics found. Nothing to load.")
        return
    client = ClickHouseClient()
    try:
        existing_keys = _get_existing_keys(client, source_rows)
        rows_to_insert = [
            [row[column] for column in COLUMNS]
            for row in source_rows
            if (
                row["match_id"],
                row["team_id"],
                row["player_id"],
            ) not in existing_keys
        ]
        if not rows_to_insert:
            print("mart_player_performance is already up to date.")
            return
        client.insert(
            TABLE,
            rows_to_insert,
            column_names=COLUMNS,
        )
        print(
            f"Loaded {len(rows_to_insert)} rows into "
            "mart_player_performance."
        )
    finally:
        client.close()


if __name__ == "__main__": run_mart_player_performance_pipeline()
