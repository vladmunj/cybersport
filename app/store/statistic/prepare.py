from services.statistics import statistics_load
from services.minio_client import MinioClient
from app.config import (MINIO_STATISTICS_BUCKET_NAME)
from app.store.team.store import team_store
from app.store.player.store import player_store
from app.store.match.prepare import get_matches_by_external_ids

def statistics_prepare():
    minio_client = MinioClient()
    statistics = statistics_load(minio_client)
    statistics_data = []
    match_ids = []
    for stat in statistics:
        stat_data = minio_client.get_json(MINIO_STATISTICS_BUCKET_NAME, stat.object_name)
        for title, team_data in stat_data['teams'].items():
            team = __store_team(team_data['info'])
            for player_data in team_data['players']:
                player = __store_player(player_data, team)
                statistics_data.append({
                    'match_id': stat_data['match_id'],
                    'player_id': player.id,
                    'rating': player_data['rating'] or None,
                    'team_id': team.id,
                })
                match_ids.append(stat_data['match_id'])
    matches = get_matches_by_external_ids(match_ids,['external_id','id'])
    match_ids_map = {
        match.external_id: match.id
        for match in matches
    }
    for item in statistics_data:
        external_id = item.pop('match_id')
        item['match_id'] = match_ids_map.get(external_id)
    return statistics_data

def __store_team(team_info):
    return team_store({
        'name': team_info['title'],
        'link': team_info['link'],
        'slug': team_info['slug'],
    })

def __store_player(player_info, team):
    return player_store({
        'nickname': player_info['nickname'],
        'fullname': player_info['fullname'],
        'team_id': team.id
    })