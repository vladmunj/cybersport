import logging
import traceback

from scraper.events import scrape_events
from scraper.matches import scrape_matches
from scraper.statistics import scrape_statistics

logger = logging.getLogger(__name__)

def alert(error, frame):
    print(f'ALERT: {error}, '
          f'filename: {frame.filename}, '
          f'line: {frame.lineno}, '
          f'code: {frame.line}, '
          f'function: {frame.name}'
    )

def main():
    try:
        scrape_events()
        scrape_matches()
        scrape_statistics()
    except Exception as e:
        logger.error(e)
        tb = traceback.extract_tb(e.__traceback__)
        frame = tb[-1]
        alert(e, frame)

if __name__ == '__main__': main()