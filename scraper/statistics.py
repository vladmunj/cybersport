from datetime import datetime
from app.config import (MINIO_MATCHES_BUCKET_NAME, MINIO_STATISTICS_BUCKET_NAME)
from services.minio_client import MinioClient
import requests as req
from bs4 import BeautifulSoup as bs

def get_players_info(data):
    players_info = []
    for player in data:
        nickname = player.select_one('[class^="playerHeader_"] span').text
        fullname = player.select_one('[class^="playerName_"]').text
        rating = player.select_one('[class^="cs2Rate_"]').text
        players_info.append({
            'nickname': nickname,
            'fullname': fullname,
            'rating': rating
        })
    return players_info

def main():
    object_date = datetime.now().strftime('%Y-%m-%d')
    minio_client = MinioClient()
    matches = minio_client.objects_list(MINIO_MATCHES_BUCKET_NAME, object_date + "/")
    for match in matches:
        match_data = minio_client.get_json(MINIO_MATCHES_BUCKET_NAME, match.object_name)
        response = req.get(match_data['link'])
        soup = bs(response.text, 'html.parser')
        teams = soup.select('[class^="teamPlayersList_"]')
        team1_data = get_players_info(teams[0])
        team2_data = get_players_info(teams[1])
        maps = soup.select('[class="scgo-stat"] [class^="card_"]')
        maps_data = []
        for map in maps:
            map_name = map.select_one('[class^="mapTitle_"]').text
            participants = map.select('[class^="participantTitle_"]')
            team1_title = participants[0].text
            team2_title = participants[1].text
            score = ':'.join(
                score_val.get_text(strip=True)
                for score_val in map.select('[class^="matchScore_"] [class^="score_"] span')
            )
            maps_data.append({
                'map_name': map_name,
                'team1': team1_title,
                'team2': team2_title,
                'score': score
            })
        match_info = {
            'match_name': match_data['title'],
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
            match.object_name.replace('.json','_statistics.json')
        )

if __name__ == '__main__': main()