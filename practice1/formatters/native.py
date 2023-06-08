from formatters.common_formatter import common_formatter
from time import time_ns as time
from sys import getsizeof


def native_serialization(data):
    start = time()
    serialized_data = str(data)
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def native_deserialization(data):
    start = time()
    deserialized_data = eval(data)
    finish = time()
    return finish - start, deserialized_data


def native_formatter(data):
    return common_formatter(data, native_serialization, native_deserialization)
