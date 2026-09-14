from sqlalchemy.inspection import inspect

def model_to_dict(instance, exclude: set[str] | None = None) -> dict:
    exclude = exclude or set()
    return {
        column.key: getattr(instance, column.key)
        for column in inspect(instance).mapper.column_attrs
        if column.key not in exclude
    }

def row_to_dict(row, exclude: set[str] | None = None) -> dict:
    exclude = exclude or set()
    return {
        key: value
        for key, value in row._mapping.items()
        if key not in exclude
    }