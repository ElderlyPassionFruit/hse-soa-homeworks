def common_formatter(data, serialization, deserialization):
    size, serialization_time, serialized_data = serialization(data)
    deserialization_time, deserialized_data = deserialization(
        serialized_data)
    return size, serialization_time, deserialization_time
