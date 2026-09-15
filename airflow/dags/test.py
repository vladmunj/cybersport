from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime


def airflow_test():
    print("HELLO FROM AIRFLOW")


with DAG(
    dag_id="airflow_test",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    test_task = PythonOperator(
        task_id="airflow_test",
        python_callable=airflow_test,
    )