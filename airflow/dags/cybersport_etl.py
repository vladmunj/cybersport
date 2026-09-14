from datetime import datetime
from airflow.sdk import DAG, task
from app.pipeline.main import run_pipeline

with DAG(
    dag_id="cybersport_etl",
    description="CS2 esports ETL pipeline",
    start_date=datetime(2026, 9, 14),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["cybersport", "etl"],
):
    @task
    def scraper_events():
        run_pipeline("scraper.events")
    @task
    def scraper_matches():
        run_pipeline("scraper.matches")
    @task
    def scraper_statistics():
        run_pipeline("scraper.statistics")
    @task
    def postgres_events():
        run_pipeline("postgres.events")
    @task
    def postgres_matches():
        run_pipeline("postgres.matches")
    @task
    def postgres_matchmap():
        run_pipeline("postgres.matchmap")
    @task
    def postgres_statistics():
        run_pipeline("postgres.statistics")
    @task
    def mart_player_performance():
        run_pipeline("clickhouse.mart_player_performance")
    @task
    def mart_match_summary():
        run_pipeline("clickhouse.mart_match_summary")
    @task
    def data_quality():
        run_pipeline("data_quality.clickhouse")

    # Dependencies
    events = scraper_events()
    matches = scraper_matches()
    statistics = scraper_statistics()

    pg_events = postgres_events()
    pg_matches = postgres_matches()
    pg_matchmap = postgres_matchmap()
    pg_statistics = postgres_statistics()

    player_mart = mart_player_performance()
    match_mart = mart_match_summary()

    dq = data_quality()

    events >> pg_events
    matches >> pg_matches
    matches >> pg_matchmap
    statistics >> pg_statistics

    pg_events >> pg_matches
    pg_matches >> pg_matchmap
    pg_matchmap >> pg_statistics

    pg_statistics >> player_mart
    pg_statistics >> match_mart

    [player_mart, match_mart] >> dq