from app.data_quality.clickhouse.runner import run_data_quality_checks

def run_clickhouse_pipeline():
    success = run_data_quality_checks()
    if not success:
        raise RuntimeError(
            "ClickHouse data quality checks failed"
        )

if __name__ == "__main__": run_clickhouse_pipeline()