from services.statistics import statistics_load
from services.minio_client import MinioClient
from app.config import (MINIO_STATISTICS_BUCKET_NAME, MAP_POOL_LIST)
from app.store.match.prepare import get_matches_by_external_ids
from app.store.map.store import map_store

def match_maps_prepare():
    minio_client = MinioClient()
    statistics = statistics_load(minio_client)
    maps_data = []
    match_ids = []
    for stat in statistics:
        stat_data = minio_client.get_json(MINIO_STATISTICS_BUCKET_NAME, stat.object_name)
        for map_data in stat_data['maps']:
            if map_data['map_name'] not in MAP_POOL_LIST: continue
            map_object = __get_map({
                'name': map_data['map_name']
            })
            maps_data.append({
                'match_id': stat_data['match_id'],
                'map_id': map_object.id,
                'score': map_data['score'],
            })
        match_ids.append(stat_data['match_id'])
    matches = get_matches_by_external_ids(match_ids,['external_id','id'])
    match_ids_map = {
        match.external_id: match.id
        for match in matches
    }
    for item in maps_data:
        external_id = item.pop('match_id')
        item['match_id'] = match_ids_map.get(external_id)
    return maps_data

def __get_map(map_data):
    return map_store(map_data)