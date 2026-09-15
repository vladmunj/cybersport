#!/bin/sh
set -e
echo "Waiting for MinIO..."
until mc alias set minio \
    http://minio:9000 \
    "$MINIO_ROOT_USER" \
    "$MINIO_ROOT_PASSWORD" \
    >/dev/null 2>&1
do
    sleep 2
done
echo "MinIO is ready."
echo "Creating buckets..."
mc mb --ignore-existing minio/airflow-logs
echo "MinIO initialization completed."