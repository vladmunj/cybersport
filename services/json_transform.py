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

def json_load_from_file(path):
    try:
        with open(path,'r',encoding='utf-8') as file:
            return json_load(file)
    except Exception as e:
        raise JsonException(e) from e
