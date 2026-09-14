from services.sentry import Sentry
from helpers.transform import row_to_dict

def transform_source_data(source_data: dict) -> list[dict]:
    matches = source_data["matches"]
    events = source_data["events"]
    events_map = {
        row.id: row
        for row in events
    }
    rows = []
    skipped_matches = []
    for match in matches:
        event = events_map.get(match.event_id)
        if event is None:
            raise ValueError(
                f"Event not found: {match.event_id}"
            )
        if match.date is None:
            skipped_matches.append(
                row_to_dict(
                    match,
                    exclude={"date"},
                )
            )
            continue
        rows.append({
            "match_id": match.id,
            "match_date": match.date,
            "event_id": event.id,
            "event_name": event.title,
            "team1": match.team1,
            "team2": match.team2,
            "score": match.score,
        })
    if skipped_matches:
        Sentry.warning(
            message="Matches skipped: date is missing",
            extra={
                "skipped_matches_count": len(skipped_matches),
                "skipped_matches": skipped_matches,
            },
            tags={
                "pipeline": "mart_match_summary",
                "reason": "missing_match_date",
            },
        )
    return rows