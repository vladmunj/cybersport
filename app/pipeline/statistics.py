from app.store.statistic.prepare import statistics_prepare
from app.store.statistic.store import statistics_store

def run_statistics_pipeline():
    prepared_data = statistics_prepare()
    statistics_store(prepared_data)

if __name__ == '__main__': run_statistics_pipeline()