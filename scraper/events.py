from app.config import (
    BASE_URL, EVENTS_SOURCE_URL, EVENTS_LIMIT,
    MINIO_EVENTS_BUCKET_NAME)
from services.minio_client import MinioClient
from services.objects import get_events_object_name
from services.http import http_req
from services.crawler import Crawler
from services.alert import report

EVENTS_CLASS_NAME_VALUE="article_"

def main():
    response = http_req(EVENTS_SOURCE_URL)
    events = __get_events(response)
    events_data = __parse_events_data(events)
    __save_events(events_data)

def __get_events(response):
    crawler = Crawler(response.text)
    return crawler.el_select(f'[class^="{EVENTS_CLASS_NAME_VALUE}"]', EVENTS_LIMIT)

def __parse_events_data(events):
    events_data = []
    for event in events:
        link = BASE_URL.rstrip('/') + '/' + event.attrs['href'].lstrip('/')
        title = event.select_one('[class^="title_"]').text
        date = event.select_one('[class^="info_"] [class^="group_"] [class^="value_"]').text
        if not all([link, title, date]):
            report({
                'error': 'event not found',
            })
            exit()
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

if __name__ == "__main__": main()