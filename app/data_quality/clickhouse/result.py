def format_check_result(check_name, condition, invalid_rows):
    return [{
        "check": check_name,
        "passed": condition,
        "invalid_rows": invalid_rows
    }]