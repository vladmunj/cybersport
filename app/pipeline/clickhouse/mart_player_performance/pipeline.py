from .extract import extract_source_data
from .transform import transform_source_data
from .load import load_to_clickhouse

def run_mart_player_performance_pipeline():
    source_data = extract_source_data()
    rows = transform_source_data(source_data)
    load_to_clickhouse(rows)

if __name__ == "__main__": run_mart_player_performance_pipeline()
