import importlib
import os
import re
from services.clickhouse import ClickHouseClient
from app.config import CLICKHOUSE_DB

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations/versions')

class MigrationRunner:

    def __init__(self):
        self.client = ClickHouseClient()
        self._create_migrations_table()

    def _create_migrations_table(self):
        self.client.command(f"""
            CREATE TABLE IF NOT EXISTS
            {CLICKHOUSE_DB}.schema_migrations
            (
                version String,
                applied_at DateTime DEFAULT now()
            )
            ENGINE = MergeTree
            ORDER BY version
        """)

    def applied(self):
        result = self.client.query(f"""
            SELECT version
            FROM {CLICKHOUSE_DB}.schema_migrations
        """)
        return {
            row[0]
            for row in result.result_rows
        }

    def get_migrations(self):
        files = os.listdir(MIGRATIONS_DIR)
        migrations = []
        for filename in files:
            match = re.match(
                r'^(\d+)_.*\.py$',
                filename
            )
            if not match: continue
            module_name = (
                'database.clickhouse.migrations.versions.'
                + filename[:-3]
            )
            module = importlib.import_module(module_name)
            migration_class = next(
                cls
                for cls in module.__dict__.values()
                if isinstance(cls, type)
                and hasattr(cls, 'version')
                and cls.__module__ == module_name
            )
            migrations.append(
                migration_class
            )
        return sorted(
            migrations,
            key=lambda migration: migration.version
        )

    def migrate(self):
        applied = self.applied()
        for migration_class in self.get_migrations():
            version = migration_class.version
            if version in applied: continue
            print(f'Applying migration: {version}')
            migration = migration_class()
            migration.upgrade(self.client)
            self.client.command(
                """
                INSERT INTO {database:Identifier}.schema_migrations
                (version)
                VALUES ({version:String})
                """,
                parameters={
                    'version': version,
                    'database': CLICKHOUSE_DB
                }
            )
            print(f'Migration {version} applied')

    def rollback(self):
        applied = self.applied()
        migrations = self.get_migrations()
        migrations = [
            migration
            for migration in migrations
            if migration.version in applied
        ]
        if not migrations:
            print('Nothing to rollback')
            return
        migration_class = sorted(
            migrations,
            key=lambda migration: migration.version
        )[-1]
        version = migration_class.version
        print(f'Rolling back migration: {version}')
        migration = migration_class()
        migration.downgrade(
            self.client
        )
        self.client.command(
            f"""
            ALTER TABLE {CLICKHOUSE_DB}.schema_migrations
            DELETE WHERE version = '{version}'
            """
        )
        print(f'Migration {version} rolled back')