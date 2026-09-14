from app.store.event.store import events_store

def run_events_pipeline():
    events_store()

if __name__ == "__main__": run_events_pipeline()