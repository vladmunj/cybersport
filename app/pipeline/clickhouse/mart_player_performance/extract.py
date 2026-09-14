from services.db import Db
from models.event import Event
from models.match import Match
from models.player import Player
from models.statistic import Statistic
from models.team import Team

def extract_source_data() -> dict:
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
    return {
        "statistics": statistics,
        "matches": matches,
        "events": events,
        "players": players,
        "teams": teams,
    }
