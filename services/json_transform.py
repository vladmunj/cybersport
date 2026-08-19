import json

def json_prepare(data):
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ).encode('utf-8')

def json_load(data):
    return json.load(data)