from services.sentry import Sentry
from helpers.transform import row_to_dict

def transform_source_data(source_data: dict) -> list[dict]:
    statistics = source_data["statistics"]
    matches = source_data["matches"]
    events = source_data["events"]
    players = source_data["players"]
    teams = source_data["teams"]
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
        if match is None: raise ValueError(f"Match not found: {statistic.match_id}")
        player = players_map.get(statistic.player_id)
        if player is None: raise ValueError(f"Player not found: {statistic.player_id}")
        team = teams_map.get(statistic.team_id)
        if team is None: raise ValueError(f"Team not found: {statistic.team_id}")
        event = events_map.get(match.event_id)
        if event is None: raise ValueError(f"Event not found: {match.event_id}")
        if match.date is None:
            skipped_matches.append(row_to_dict(match,exclude={"date"}))
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
            "rating": (
                float(statistic.rating)
                if statistic.rating is not None
                else 0.0
            ),
        })
    if skipped_matches:
        Sentry.warning(
            message="Match skipped: date is missing",
            extra={
                "skipped_matches_count": len(skipped_matches),
                "skipped_matches": skipped_matches,
            },
            tags={
                "pipeline": "mart_player_performance",
                "reason": "missing_match_date",
            },
        )
    return rows
