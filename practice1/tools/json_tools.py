import json

def serialize(data):
    return json.dumps(data)

def deserialize(data):
    try:
        result = json.loads(data)
        return result
    except:
        return None
