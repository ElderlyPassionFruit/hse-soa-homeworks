import os
from formatters.get_formatter_by_name import get_formatter_by_name

test_data = {
    "int": 17957,
    "float": 3.1415926,
    "string": "string",
    "bool": False,
    "dict": {"key1": "value", "key2": "2", "key3": "True"},
    "list": ["first_string", "second_string", "third_string", "abacabadabacaba"]
}


class Worker:
    def __init__(self):
        format = os.getenv("FORMAT")
        self.format = format
        self.formatter = get_formatter_by_name(format)
        self.iters = int(os.getenv("ITERS"))

    def do_test(self):
        total_size = 0
        total_serialize_time = 0
        total_deserialize_time = 0
        for _ in range(self.iters):
            size, serialize_time, deserialize_time = self.formatter(test_data)
            total_size += size
            total_serialize_time += serialize_time
            total_deserialize_time += deserialize_time
        return f"format: {self.format}, serialized size: {round(total_size / self.iters)} bytes, avg serialization time: {round(total_serialize_time / self.iters)} ns, avg deserialization time: {round(total_deserialize_time / self.iters)} ns"
