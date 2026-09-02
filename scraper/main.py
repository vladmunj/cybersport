import traceback

from scraper.events import scrape_events
from scraper.matches import scrape_matches
from scraper.statistics import scrape_statistics
from services.logger import Logger

def alert(error, frame):
    print(f'ALERT: {error}, '
          f'filename: {frame.filename}, '
          f'line: {frame.lineno}, '
          f'code: {frame.line}, '
          f'function: {frame.name}'
    )

def main():
    __logger = Logger()
    try:
        scrape_events()
        scrape_matches()
        scrape_statistics()
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        frame = tb[-1]
        alert(e, frame)
        __logger.exception(e)
        raise

if __name__ == '__main__': main()