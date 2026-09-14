from services.clickhouse import ClickHouseClient
from app.config import CLICKHOUSE_DB
from .result import format_check_result

PLAYER_MART = (
    f"{CLICKHOUSE_DB}.mart_player_performance"
)
MATCH_MART = (
    f"{CLICKHOUSE_DB}.mart_match_summary"
)

def check_player_performance_not_null(
    client: ClickHouseClient,
) -> list[dict]:
    result = client.query(
        f"""
        SELECT
            count() AS invalid_rows
        FROM {PLAYER_MART}
        WHERE
            match_id IS NULL
            OR event_id IS NULL
            OR team_id IS NULL
            OR player_id IS NULL
            OR match_date IS NULL
        """
    )
    invalid_rows = result.result_rows[0][0]
    return format_check_result(
        "player_performance_not_null",
        invalid_rows == 0,
        invalid_rows
    )

def check_player_performance_duplicates(
    client: ClickHouseClient,
) -> list[dict]:
    result = client.query(
        f"""
        SELECT count()
        FROM
        (
            SELECT
                match_id,
                team_id,
                player_id
            FROM {PLAYER_MART}
            GROUP BY
                match_id,
                team_id,
                player_id
            HAVING count() > 1
        )
        """
    )
    duplicates = result.result_rows[0][0]
    return format_check_result(
        "player_performance_duplicates",
        duplicates == 0,
        duplicates
    )

def check_rating_range(
    client: ClickHouseClient,
) -> list[dict]:
    result = client.query(
        f"""
        SELECT count()
        FROM {PLAYER_MART}
        WHERE rating < 0
        """
    )
    invalid_rows = result.result_rows[0][0]
    return format_check_result(
        "rating_range",
        invalid_rows == 0,
        invalid_rows
    )

def check_match_summary_duplicates(
    client: ClickHouseClient,
) -> list[dict]:
    result = client.query(
        f"""
        SELECT count()
        FROM
        (
            SELECT match_id
            FROM {MATCH_MART}
            GROUP BY match_id
            HAVING count() > 1
        )
        """
    )
    duplicates = result.result_rows[0][0]
    return format_check_result(
        "match_summary_duplicates",
        duplicates == 0,
        duplicates
    )

def check_match_summary_not_empty(
    client: ClickHouseClient,
) -> list[dict]:
    result = client.query(
        f"""
        SELECT count()
        FROM {MATCH_MART}
        """
    )
    rows = result.result_rows[0][0]
    return format_check_result(
        "match_summary_not_empty",
        rows > 0,
        0 if rows > 0 else rows
    )