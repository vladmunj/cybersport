#!/bin/bash
set -e
MIGRATIONS_DIR="migrations/versions"
if [ -z "$1" ]; then
    echo "Usage: ./migrate.sh \"table name\""
    exit 1
fi
MIGRATION_NAME="create $1 table"
SLUG=$(echo "$MIGRATION_NAME" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/ /_/g')
echo "Checking existing migrations..."
if find "$MIGRATIONS_DIR" -type f -name "*_${SLUG}.py" | grep -q .; then
    echo "Migration '$MIGRATION_NAME' already exists."
    exit 1
fi
echo "Creating migration: $MIGRATION_NAME"
alembic revision --autogenerate -m "$MIGRATION_NAME"
echo "Applying migration..."
alembic upgrade head
echo "Migration completed successfully."