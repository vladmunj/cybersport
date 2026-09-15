from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from app.pipeline.main import run_pipeline

def run_pipeline_task(pipeline_name: str) -> None:
    run_pipeline(pipeline_name)

with DAG(
    dag_id="cybersport_etl",
    description="CS2 esports ETL pipeline",
    start_date=datetime(2026, 9, 14),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["cybersport", "etl"],
) as dag:
    scraper_events = PythonOperator(
        task_id="scraper_events",
        python_callable=lambda: print("EVENTS TEST"),
        # python_callable=run_pipeline_task,
        # op_kwargs={"pipeline_name": "scraper.events"},
    )
    scraper_matches = PythonOperator(
        task_id="scraper_matches",
        python_callable=lambda: print("MATCHES TEST"),
        # python_callable=run_pipeline_task,
        # op_kwargs={"pipeline_name": "scraper.matches"},
    )
    scraper_statistics = PythonOperator(
        task_id="scraper_statistics",
        python_callable=lambda: print("STATISTICS TEST"),
        # python_callable=run_pipeline_task,
        # op_kwargs={"pipeline_name": "scraper.statistics"},
    )
    postgres_events = PythonOperator(
        task_id="postgres_events",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "postgres.events"},
    )
    postgres_matches = PythonOperator(
        task_id="postgres_matches",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "postgres.matches"},
    )
    postgres_matchmap = PythonOperator(
        task_id="postgres_matchmap",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "postgres.matchmap"},
    )
    postgres_statistics = PythonOperator(
        task_id="postgres_statistics",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "postgres.statistics"},
    )
    mart_player_performance = PythonOperator(
        task_id="mart_player_performance",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "clickhouse.mart_player_performance"},
    )
    mart_match_summary = PythonOperator(
        task_id="mart_match_summary",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "clickhouse.mart_match_summary"},
    )
    data_quality = PythonOperator(
        task_id="data_quality",
        python_callable=run_pipeline_task,
        op_kwargs={"pipeline_name": "data_quality.clickhouse"},
    )

    scraper_events >> postgres_events
    scraper_matches >> postgres_matches
    scraper_matches >> postgres_matchmap
    scraper_statistics >> postgres_statistics

    postgres_events >> postgres_matches
    postgres_matches >> postgres_matchmap
    postgres_matchmap >> postgres_statistics

    postgres_statistics >> mart_player_performance
    postgres_statistics >> mart_match_summary

    [mart_player_performance, mart_match_summary] >> data_quality