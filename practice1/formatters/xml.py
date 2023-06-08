from xmltodict import parse as deserialize
from dicttoxml import dicttoxml as serialize

from time import time_ns as time
from sys import getsizeof
from formatters.common_formatter import common_formatter


def xml_serialization(data):
    start = time()
    serialized_data = serialize(data)
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def xml_deserialization(data):
    start = time()
    deserialized_data = deserialize(data)
    finish = time()
    return finish - start, deserialized_data


def xml_formatter(data):
    return common_formatter(data, xml_serialization, xml_deserialization)
