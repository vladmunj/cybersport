from services.events import events_load
from services.minio_client import MinioClient
from datetime import datetime

def events_prepare():
    minio_client = MinioClient()
    events = events_load(minio_client)
    for event in events:
        start_date = datetime.strptime(
            event["date"].split("-")[0].strip(),
            "%d.%m.%Y"
        ).strftime('%Y-%m-%d')
        end_date = datetime.strptime(
            event["date"].split("-")[1].strip(),
            "%d.%m.%Y"
        ).strftime('%Y-%m-%d')
        yield {
            'title': event['title'],
            'link': event['link'],
            'slug': event['slug'],
            'start_date': start_date,
            'end_date': end_date
        }