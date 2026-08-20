from app.config import (
    BASE_URL, EVENTS_SOURCE_URL, EVENTS_LIMIT,
    MINIO_EVENTS_BUCKET_NAME)
import requests as req
from bs4 import BeautifulSoup as bs
from services.minio_client import MinioClient
from services.objects import get_events_object_name

EVENTS_CLASS_NAME_VALUE="article_"

def main():
    response = req.get(EVENTS_SOURCE_URL)
    soup = bs(response.text, 'html.parser')
    events = soup.select(f'[class^="{EVENTS_CLASS_NAME_VALUE}"]', limit=EVENTS_LIMIT)
    events_data = []
    for event in events:
        link = BASE_URL.rstrip('/') + '/' + event.attrs['href'].lstrip('/')
        title = event.select_one('[class^="title_"]').text
        date = event.select_one('[class^="info_"] [class^="group_"] [class^="value_"]').text
        events_data.append({
            'title': title,
            'link': link,
            'date': date
        })
    object_name = get_events_object_name()
    minio_client = MinioClient()
    minio_client.upload_json(MINIO_EVENTS_BUCKET_NAME, events_data, object_name)

if __name__ == "__main__": main()