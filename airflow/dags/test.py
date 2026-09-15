from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def test_logging():
    print("Testing Airflow remote logging to MinIO")
    print("Second log line")
    print("Third log line")


with DAG(
    dag_id="test_minio_logging",
    start_date=datetime(2026, 9, 15),
    schedule=None,
    catchup=False,
) as dag:
    test_task = PythonOperator(
        task_id="test_logging",
        python_callable=test_logging,
    )