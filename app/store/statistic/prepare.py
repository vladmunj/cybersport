from services.statistics import statistics_load
from services.minio_client import MinioClient
from app.config import (MINIO_STATISTICS_BUCKET_NAME)
from app.store.team.prepare import prepare_team
from app.store.player.prepare import prepare_player

def statistics_prepare():
    minio_client = MinioClient()
    statistics = statistics_load(minio_client)
    result = {
        'teams': [],
        'players': [],
        'statistics': [],
        'match_external_ids': []
    }
    for stat in statistics:
        stat_data = minio_client.get_json(MINIO_STATISTICS_BUCKET_NAME, stat.object_name)
        match_external_id = stat_data['match_id']
        result['match_external_ids'].append(match_external_id)
        for _, team_data in stat_data['teams'].items():
            team = prepare_team(team_data['info'])
            result['teams'].append(team)
            for player_data in team_data['players']:
                player = prepare_player(player_data, team['slug'])
                result['players'].append(player)
                result['statistics'].append({
                    'match_external_id': match_external_id,
                    'player_nickname': player['nickname'],
                    'team_slug': team['slug'],
                    'rating': player_data['rating'] or None,
                })
    return result