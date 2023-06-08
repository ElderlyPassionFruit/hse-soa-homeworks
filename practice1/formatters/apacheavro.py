import avro.schema
from avro.io import DatumWriter, BinaryEncoder, DatumReader, BinaryDecoder
from io import BytesIO

from formatters.common_formatter import common_formatter
from time import time_ns as time
from sys import getsizeof

schema_path = "formatters/test_data.avsc"
avro_schema = avro.schema.parse(open(schema_path).read().replace('\n', ''))


def apacheavro_serialization(data):
    start = time()
    buf = BytesIO()
    writer = DatumWriter(avro_schema)
    writer.write(data, BinaryEncoder(buf))
    serialized_data = buf.getvalue()
    finish = time()
    return getsizeof(serialized_data), finish - start, serialized_data


def apacheavro_deserialization(data):
    start = time()
    reader = DatumReader(avro_schema)
    deserialized_data = reader.read(BinaryDecoder(BytesIO(data)))
    finish = time()
    return finish - start, deserialized_data


def apacheavro_formatter(data):
    return common_formatter(data, apacheavro_serialization, apacheavro_deserialization)
