from datetime import datetime
from app.config import (MINIO_MATCHES_BUCKET_NAME, MINIO_STATISTICS_BUCKET_NAME)
from exceptions.crawl import CrawlException
from services.minio_client import MinioClient
from services.http import http_req
from services.crawler import Crawler

def get_players_info(data):
    players_info = []
    for player in data:
        nickname = Crawler.text(player, '[class^="playerHeader_"] span')
        fullname = Crawler.text(player, '[class^="playerName_"]')
        rating = Crawler.text(player, '[class^="cs2Rate_"]')
        players_info.append({
            'nickname': nickname,
            'fullname': fullname,
            'rating': rating
        })
    return players_info

def scrape_statistics():
    minio_client = MinioClient()
    matches = __get_matches(minio_client)
    __process_stats(minio_client, matches)

def __get_matches(minio_client):
    object_date = datetime.now().strftime('%Y-%m-%d')
    return minio_client.objects_list(MINIO_MATCHES_BUCKET_NAME, object_date + "/")

def __process_stats(minio_client, matches):
    for match in matches:
        match_data = minio_client.get_json(MINIO_MATCHES_BUCKET_NAME, match.object_name)
        response = http_req(match_data['link'])
        teams = Crawler.root_select(response.text, '[class^="teamPlayersList_"]')
        if len(teams) != 2:
            raise CrawlException({'error': f'Expected 2 teams, got {len(teams)}'})
        team1_data = get_players_info(teams[0])
        team2_data = get_players_info(teams[1])
        maps = Crawler.root_select(response.text, '[class="scgo-stat"] [class^="card_"]')
        maps_data = []
        for map_info in maps:
            map_name = Crawler.text(map_info, '[class^="mapTitle_"]')
            participants = Crawler.select(map_info, '[class^="participantTitle_"]')
            if len(participants) != 2:
                raise CrawlException(f'Expected 2 participants, got {len(participants)}')
            team1_title = participants[0].get_text(strip = True)
            team2_title = participants[1].get_text(strip = True)
            score = ':'.join(
                score_val.get_text(strip=True)
                for score_val in Crawler.select(
                    map_info,
                    '[class^="matchScore_"] [class^="score_"] span'
                )
            )
            maps_data.append({
                'map_name': map_name,
                'team1': team1_title,
                'team2': team2_title,
                'score': score
            })
        __upload_match_info(minio_client, match, match_data, maps_data, team1_data, team2_data)

def __upload_match_info(minio_client, match,
                        match_data, maps_data, team1_data, team2_data):
    match_info = {
        'match_id': match_data['id'],
        'opposing_teams': match_data['team1'] + ' vs ' + match_data['team2'],
        'teams': {
            match_data['team1']: {
                'players': team1_data
            },
            match_data['team2']: {
                'players': team2_data
            }
        },
        'maps': maps_data
    }
    minio_client.upload_json(
        MINIO_STATISTICS_BUCKET_NAME,
        match_info,
        match.object_name.replace('.json', '_statistics.json')
    )

if __name__ == '__main__': scrape_statistics()