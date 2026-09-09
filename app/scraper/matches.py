from app.config import (BASE_URL,
                        MINIO_MATCHES_BUCKET_NAME)
from services.minio_client import MinioClient
from services.objects import get_matches_object_name
from services.http import http_req
from services.crawler import Crawler
from services.url import extract_match_id
from services.events import events_load

MATCHES_CLASS_VALUE="battleRoyale_"

def scrape_matches():
    minio_client = MinioClient()
    events = events_load(minio_client)
    for match_data in __get_matches(events):
        __upload_match(minio_client, match_data)

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
                'slug': event['slug']
            }

def __get_match_link(match):
    match_link_el = Crawler.select_one(match, '[class^="matchLink_"]')
    link_attr = Crawler.attr(match_link_el, 'href')
    return BASE_URL.rstrip('/') + '/' + link_attr.lstrip('/')

def __upload_match(minio_client, match_data):
    match_object_name = get_matches_object_name(
        match_data['slug'],
        match_data['id']
    )
    minio_client.upload_json(
        MINIO_MATCHES_BUCKET_NAME,
        match_data,
        match_object_name
    )

if __name__ == "__main__": scrape_matches()