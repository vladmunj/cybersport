#!/bin/bash
set -e
echo "Rolling back ClickHouse migration..."
python -m database.clickhouse rollback
echo "ClickHouse rollback completed."