from app.config import (
    BASE_URL, EVENTS_SOURCE_URL, EVENTS_LIMIT,
    MINIO_EVENTS_BUCKET_NAME)
from services.minio_client import MinioClient
from services.objects import get_events_object_name
from services.http import http_req
from services.crawler import Crawler

EVENTS_CLASS_NAME_VALUE="article_"

def scrape_events():
    response = http_req(EVENTS_SOURCE_URL)
    events = __get_events(response)
    events_data = __parse_events_data(events)
    __save_events(events_data)

def __get_events(response):
    return Crawler.root_select(
        response.text,
        f'[class^="{EVENTS_CLASS_NAME_VALUE}"]',
        EVENTS_LIMIT
    )

def __parse_events_data(events):
    events_data = []
    for event in events:
        href = Crawler.attr(event, 'href')
        link = BASE_URL.rstrip('/') + '/' + href.lstrip('/')
        title = Crawler.text(event, '[class^="title_"]')
        date = Crawler.text(event, '[class^="info_"] [class^="group_"] [class^="value_"]')
        events_data.append({
            'title': title,
            'link': link,
            'date': date
        })
    return events_data

def __save_events(events_data):
    object_name = get_events_object_name()
    minio_client = MinioClient()
    minio_client.upload_json(MINIO_EVENTS_BUCKET_NAME, events_data, object_name)

if __name__ == "__main__": scrape_events()