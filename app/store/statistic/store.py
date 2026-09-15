from services.db import Db
from models.statistic import Statistic
from models.match import Match
from app.store.team.store import team_store
from app.store.player.store import player_store

def statistics_store(data):
    teams_map = {}
    players_map = {}
    for team_data in data['teams']:
        team = team_store(team_data)
        teams_map[team.slug] = team.id
    for player_data in data['players']:
        team_id = teams_map.get(player_data['team_slug'])
        if team_id is None:
            raise ValueError(
                f"Team not found: {player_data['team_slug']}"
            )
        player = player_store({
            'nickname': player_data['nickname'],
            'fullname': player_data['fullname'],
            'team_id': team_id,
        })
        players_map[(player.nickname, team_id)] = player.id
    matches = (Db.query(Match)
               .select(['id','external_id'])
               .where_in('external_id', data['match_external_ids'])
               .get()
    )
    matches_map = {
        match.external_id: match.id
        for match in matches
    }
    statistics = []
    for item in data['statistics']:
        match_id = matches_map.get(item['match_external_id'])
        team_id = teams_map.get(item['team_slug'])
        player_id = players_map.get((item['player_nickname'], team_id))
        if match_id is None: raise ValueError(f"Match not found: {item['match_external_id']}")
        if team_id is None: raise ValueError(f"Team not found: {item['team_slug']}")
        if player_id is None: raise ValueError(f"Player not found: {item['player_nickname']}")
        statistics.append({
            'match_id': match_id,
            'player_id': player_id,
            'team_id': team_id,
            'rating': item['rating'],
        })
    Db.save_many_by_keys(
        model=Statistic,
        records=statistics,
        keys=['match_id','player_id','team_id']
    )