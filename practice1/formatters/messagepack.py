from msgpack import packb as serialize, unpackb as deserialize

from time import time_ns as time
from sys import getsizeof
from formatters.common_formatter import common_formatter


def messagepack_serialization(data):
    start = time()
    serialized_data = serialize(data)
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def messagepack_deserialization(data):
    start = time()
    deserialized_data = deserialize(data)
    finish = time()
    return finish - start, deserialized_data


def messagepack_formatter(data):
    return common_formatter(data, messagepack_serialization, messagepack_deserialization)
