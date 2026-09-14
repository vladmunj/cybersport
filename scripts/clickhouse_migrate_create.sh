#!/bin/bash
set -e
MIGRATIONS_DIR="database/clickhouse/migrations/versions"
if [ -z "$1" ]; then
    echo "Usage: ./clickhouse_migrate_create.sh \"migration name\""
    exit 1
fi
MIGRATION_NAME="$1"
SLUG=$(echo "$MIGRATION_NAME" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/ /_/g')
echo "Checking existing migrations..."
if find "$MIGRATIONS_DIR" \
    -type f \
    -name "*_${SLUG}.py" \
    | grep -q .; then
    echo "Migration '$MIGRATION_NAME' already exists."
    exit 1
fi
LAST_VERSION=$(find "$MIGRATIONS_DIR" \
    -type f \
    -name '[0-9]*_*.py' \
    | sed -E 's/.*\/([0-9]+)_.*/\1/' \
    | sort -n \
    | tail -1)
if [ -z "$LAST_VERSION" ]; then
    NEXT_VERSION=1
else
    NEXT_VERSION=$((10#$LAST_VERSION + 1))
fi
VERSION=$(printf "%03d" "$NEXT_VERSION")
FILE="$MIGRATIONS_DIR/${VERSION}_${SLUG}.py"
echo "Creating migration:"
echo "$FILE"
cat > "$FILE" <<EOF
from database.clickhouse.base import Migration

class Migration${VERSION}(Migration):
    version = '${VERSION}'
    def upgrade(self, client):
        client.command("""
            -- TODO: migration
        """)

    def downgrade(self, client):
        client.command("""
            -- TODO: rollback
        """)
EOF

echo "Migration created successfully."