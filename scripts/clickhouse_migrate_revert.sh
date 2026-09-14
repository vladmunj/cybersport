#!/bin/bash
set -e
echo "Rolling back ClickHouse migration..."
python -m migrations.clickhouse rollback
echo "ClickHouse rollback completed."