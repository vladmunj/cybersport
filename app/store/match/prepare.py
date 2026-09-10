from models import event
from services.matches import matches_load
from services.minio_client import MinioClient
from datetime import datetime, date
from services.db import Db
from models.event import Event
from app.config import (MINIO_MATCHES_BUCKET_NAME)

def matches_prepare():
    minio_client = MinioClient()
    matches = matches_load(minio_client)
    events = (Db.query(Event)
              .select(['slug','id'])
              .where_date("created_at",date.today())
              .get())
    events_map = {
        event.slug: event.id
        for event in events
    }
    matches_data = []
    for match in matches:
        match_data = minio_client.get_json(MINIO_MATCHES_BUCKET_NAME, match.object_name)
        date_formatted = datetime.strptime(
            match_data["date"],
            "%d.%m.%y в %H:%M"
        ).strftime('%Y-%m-%d %H:%M:%S')
        event_id = events_map.get(match_data['slug'])
        matches_data.append({
            'external_id': match_data['id'],
            'event_id': event_id,
            'date': date_formatted,
            'team1': match_data['team1'],
            'team2': match_data['team2'],
            'score': match_data['score'],
            'link': match_data['link'],
        })
    return matches_data