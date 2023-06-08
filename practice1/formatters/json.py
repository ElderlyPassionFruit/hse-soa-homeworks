import json

from formatters.common_formatter import common_formatter
from time import time_ns as time
from sys import getsizeof


def json_serialization(data):
    start = time()
    serialized_data = json.dumps(data)
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def json_deserialization(data):
    start = time()
    deserialized_data = json.loads(data)
    finish = time()
    return finish - start, deserialized_data


def json_formatter(data):
    return common_formatter(data, json_serialization, json_deserialization)
