from app.scraper.events import scrape_events

def run_events_pipeline():
    scrape_events()

if __name__ == '__main__': run_events_pipeline()