import datetime
import traceback
import sentry_sdk
from app.config import (
    SENTRY_DSN, SENTRY_ENVIRONMENT, SENTRY_TRACES_SAMPLE_RATE)

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

def __sentry_init():
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE
    )
    snapshot_date = datetime.datetime.now().strftime('%Y%m%d')
    sentry_sdk.set_tag('snapshot_date', snapshot_date)

def main():
    __logger = Logger()
    __sentry_init()
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