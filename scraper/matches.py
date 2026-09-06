from app.config import (MINIO_EVENTS_BUCKET_NAME, BASE_URL,
                        MINIO_MATCHES_BUCKET_NAME)
from services.minio_client import MinioClient
from services.objects import get_events_object_name, get_matches_object_name
from datetime import datetime
from services.http import http_req
from services.crawler import Crawler
from services.url import extract_match_id

MATCHES_CLASS_VALUE="battleRoyale_"

def scrape_matches():
    minio_client = MinioClient()
    events = __get_events(minio_client)
    for match_data in __get_matches(events):
        __upload_match(minio_client, match_data)

def __get_events(minio_client):
    events_object_name = get_events_object_name()
    return minio_client.get_json(
        MINIO_EVENTS_BUCKET_NAME,
        events_object_name
    )

def __get_matches(events):
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
            link = __get_match_link(match)
            match_id = extract_match_id(link)
            yield {
                'date': date,
                'team1': team1,
                'team2': team2,
                'score': score,
                'link': link,
                'id': match_id,
                'title': event['title']
            }

def __get_match_link(match):
    match_link_el = Crawler.select_one(match, '[class^="matchLink_"]')
    link_attr = Crawler.attr(match_link_el, 'href')
    return BASE_URL.rstrip('/') + '/' + link_attr.lstrip('/')

def __upload_match(minio_client, matches_data):
    object_name_date = (datetime
                        .strptime(matches_data['date'], '%d.%m.%y в %H:%M')
                        .strftime('%Y-%m-%d'))
    match_object_name = get_matches_object_name(
        matches_data['title'].replace(' ', '_'),
        object_name_date,
        matches_data['team1'] + "_vs_" + matches_data['team2']
    )
    minio_client.upload_json(
        MINIO_MATCHES_BUCKET_NAME,
        matches_data,
        match_object_name
    )

if __name__ == "__main__": scrape_matches()