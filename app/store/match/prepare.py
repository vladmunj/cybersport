from services.matches import matches_load
from services.minio_client import MinioClient
from datetime import datetime
from services.db import Db
from models.event import Event
from app.config import (MINIO_MATCHES_BUCKET_NAME)
from models.match import Match

def matches_prepare():
    minio_client = MinioClient()
    matches = matches_load(minio_client)
    matches_data = []
    match_slugs = set()
    for match in matches:
        match_data = minio_client.get_json(MINIO_MATCHES_BUCKET_NAME, match.object_name)
        try:
            date_formatted = datetime.strptime(
                match_data["date"],
                "%d.%m.%y в %H:%M"
                ).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            date_formatted = None
        match_slugs.add(match_data["slug"])
        matches_data.append({
            'external_id': match_data['id'],
            'slug': match_data['slug'],
            'date': date_formatted,
            'team1': match_data['team1'],
            'team2': match_data['team2'],
            'score': match_data['score'],
            'link': match_data['link'],
        })
    events = (Db.query(Event)
              .select(['slug', 'id'])
              .where_in("slug", list(match_slugs))
              .get())
    events_map = {
        event.slug: event.id
        for event in events
    }
    for match_item in matches_data:
        slug = match_item.pop('slug')
        event_id = events_map.get(slug)
        if event_id is None:
            raise ValueError(f"Event {slug} not found")
        match_item['event_id'] = event_id
    return matches_data

def get_matches_by_external_ids(ids, select_fields):
    return Db.query(Match).select(select_fields).where_in('external_id', ids).get()