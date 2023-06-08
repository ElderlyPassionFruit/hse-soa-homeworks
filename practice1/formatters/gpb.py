from formatters.test_data_pb2 import TestData

from sys import getsizeof
from time import time_ns as time
from formatters.common_formatter import common_formatter


def pack_data(input):
    data = TestData(
        int=input["int"],
        float=input["float"],
        string=input["string"],
        bool=input["bool"],
        dict=input["dict"],
        list=input["list"]
    )
    return data.SerializeToString()


def unpack_data(serialized_data):
    data = TestData()
    data.ParseFromString(serialized_data)
    return data


def gpb_serialization(data):
    start = time()
    serialized_data = pack_data(data)
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def gpb_deserialization(data):
    start = time()
    deserialized_data = unpack_data(data)
    finish = time()
    return finish - start, deserialized_data


def gpb_formatter(data):
    return common_formatter(data, gpb_serialization, gpb_deserialization)
