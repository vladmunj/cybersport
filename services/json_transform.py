import json
from exceptions.json import JsonException

def json_prepare(data):
    try:
        return json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ).encode('utf-8')
    except Exception as e:
        raise JsonException(e) from e

def json_load(data):
    try:
        return json.load(data)
    except Exception as e:
        raise JsonException(e) from e