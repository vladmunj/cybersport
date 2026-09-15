FROM apache/airflow:3.3.1
USER root
COPY requirements.txt /requirements.txt
USER airflow
RUN python -m pip install --no-cache-dir -r /requirements.txt