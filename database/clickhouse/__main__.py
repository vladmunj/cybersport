import sys
from database.clickhouse.runner import MigrationRunner

def main():
    if len(sys.argv) < 2:
        print(
            'Usage: '
            'python -m database.clickhouse '
            '[migrate|rollback]'
        )
        sys.exit(1)
    command = sys.argv[1]
    runner = MigrationRunner()
    if command == 'migrate': runner.migrate()
    elif command == 'rollback': runner.rollback()
    else:
        print(f'Unknown command: {command}')
        sys.exit(1)

if __name__ == '__main__': main()