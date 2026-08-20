from datetime import datetime

def events_object_name():
    object_date = datetime.now().strftime('%Y-%m-%d')
    return f"{object_date}/events.json"

def matches_object_name(event_title, date, match_name):
    object_date = datetime.now().strftime('%Y-%m-%d')
    return f"{object_date}/{event_title}/{date}/{match_name}.json"