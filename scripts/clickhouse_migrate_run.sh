#!/bin/bash
set -e
echo "Applying ClickHouse migrations..."
python -m database.clickhouse migrate
echo "ClickHouse migrations completed."