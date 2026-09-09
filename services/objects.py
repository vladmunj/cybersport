from datetime import datetime

def get_events_object_name():
    object_date = datetime.now().strftime('%Y-%m-%d')
    return f"{object_date}/events.json"

def get_matches_object_name(event_slug, match_id):
    object_date = datetime.now().strftime('%Y-%m-%d')
    return f"{object_date}/{event_slug}/{match_id}.json"