from app.store.event.prepare import events_prepare
from services.db import Db
from models.event import Event

def events_store():
    for event_data in events_prepare():
        __event_store(event_data)

def __event_store(event_data):
    Db.save(model=Event,data=event_data,key='slug')

if __name__ == "__main__": events_store()