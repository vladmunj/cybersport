from app.config import (MINIO_EVENTS_BUCKET_NAME, BASE_URL,
                        MINIO_MATCHES_BUCKET_NAME)
from services.minio_client import MinioClient
from services.objects import get_events_object_name, get_matches_object_name
from datetime import datetime
from services.http import http_req
from services.crawler import Crawler

MATCHES_CLASS_VALUE="battleRoyale_"

def scrape_matches():
    minio_client = MinioClient()
    events = __get_events(minio_client)
    __get_matches(events, minio_client)

def __get_events(minio_client):
    events_object_name = get_events_object_name()
    return minio_client.get_json(
        MINIO_EVENTS_BUCKET_NAME,
        events_object_name
    )

def __get_matches(events, minio_client):
    for event in events:
        response = http_req(event['link'])
        matches = Crawler.root_select(response.text, f'[class*="{MATCHES_CLASS_VALUE}"]')
        for match in matches:
            date = Crawler.text(match, '[class^="date_"]')
            team1 = Crawler.text(match, '[class*="participant1_"] [class^="titleWrapper_"] [class^="title_"]')
            team2 = Crawler.text(match, '[class*="participant2_"] [class^="titleWrapper_"] [class^="title_"]')
            score_block = Crawler.select_one(match, '[class^="score_"]')
            score = ''.join(
                value.get_text(strip=True)
                for value in Crawler.select(score_block,'span')
            )
            link = (BASE_URL.rstrip('/') + '/'
                    + Crawler.get(
                        match.select_one('[class^="matchLink_"]').attrs['href'],
                        'Element with class matching [class^="matchLink_"] and href attr not found'
                    ).lstrip('/'))
            matches_data = {
                'date': date,
                'team1': team1,
                'team2': team2,
                'score': score,
                'link': link,
                'title': event['title']
            }
            __upload_matches(event, minio_client, matches_data)

def __upload_matches(event, minio_client, matches_data):
    object_name_date = (datetime
                        .strptime(matches_data['date'], '%d.%m.%y в %H:%M')
                        .strftime('%Y-%m-%d'))
    match_object_name = get_matches_object_name(
        event['title'].replace(' ', '_'),
        object_name_date,
        matches_data['team1'] + "_vs_" + matches_data['team2']
    )
    minio_client.upload_json(
        MINIO_MATCHES_BUCKET_NAME,
        matches_data,
        match_object_name
    )

if __name__ == "__main__": scrape_matches()