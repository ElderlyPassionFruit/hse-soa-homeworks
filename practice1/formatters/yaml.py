from yaml import safe_dump as serialize, safe_load as deserialize

from time import time_ns as time
from sys import getsizeof
from formatters.common_formatter import common_formatter


def yaml_serialization(data):
    start = time()
    serialized_data = serialize(data)
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def yaml_deserialization(data):
    start = time()
    deserialized_data = deserialize(data)
    finish = time()
    return finish - start, deserialized_data


def yaml_formatter(data):
    return common_formatter(data, yaml_serialization, yaml_deserialization)
