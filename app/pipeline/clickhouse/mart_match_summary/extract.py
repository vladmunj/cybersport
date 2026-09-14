from services.db import Db
from models.event import Event
from models.match import Match

def extract_source_data() -> dict:
    matches = Db.query(Match).select([
        "id",
        "external_id",
        "event_id",
        "date",
        "team1",
        "team2",
        "score",
        "link",
    ]).get()
    events = Db.query(Event).select([
        "id",
        "title",
    ]).get()
    return {
        "matches": matches,
        "events": events,
    }