from services.clickhouse import ClickHouseClient
from .checks import (
    check_player_performance_not_null,
    check_player_performance_duplicates,
    check_rating_range,
    check_match_summary_duplicates,
    check_match_summary_not_empty,
)

def run_data_quality_checks() -> bool:
    client = ClickHouseClient()
    try:
        checks = [
            check_player_performance_not_null,
            check_player_performance_duplicates,
            check_rating_range,
            check_match_summary_duplicates,
            check_match_summary_not_empty,
        ]
        results = []
        for check in checks:
            results.extend(check(client))
        all_passed = True
        print()
        print("=" * 70)
        print("DATA QUALITY")
        print("=" * 70)
        for result in results:
            status = (
                "PASS"
                if result["passed"]
                else "FAIL"
            )
            print(
                f"[{status}] "
                f"{result['check']} "
                f"(invalid: {result['invalid_rows']})"
            )
            if not result["passed"]:
                all_passed = False
        print("=" * 70)
        if all_passed:
            print("All data quality checks passed.")
        else:
            print("Data quality checks failed.")
        return all_passed
    finally:
        client.close()

if __name__ == "__main__":
    success = run_data_quality_checks()
    if not success:
        raise SystemExit(1)