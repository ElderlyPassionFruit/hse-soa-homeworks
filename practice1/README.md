## Сборка контейнера

```docker build -f env.Dockerfile -t elderlypassionfruit/soa1-env .```

## Запуск

```docker-copmose up```

### API

proxy слушает ```0.0.0.0:2000```, поддерживает 2 типа запросов:

* ```{"message_type": "get_result", "formats": [...]}```, где в списке ```formats``` должно быть произвольное непустое подмножество из списка ```["native", "json", "xml", "yaml", "messagepack", "gpb", "apacheavro"]``` (чувствительно к регистру).

* ```{"message_type": "get_result_all"}```

В случае первого запроса, для каждого указанного формата вернёт ответным сообщением результат тестирования на данном формате. В случае второго запроса - для всех имеющихся форматов.

Формат сообщения - Тип, размер в сериализованном виде в байтах, среднее время сериализации в наносекундах, среднее время десериализации в наносекундах

Пример:

```
native, serialized size: 252 bytes, avg serialization time: 5954 ns, avg deserialization time: 58690 ns

xml, serialized size: 493 bytes, avg serialization time: 
910313 ns, avg deserialization time: 105108 ns

messagepack, serialized size: 172 bytes, avg serialization time: 3207 ns, avg deserialization time: 3634 ns from

json, serialized size: 252 bytes, avg serialization time: 7571 ns, avg deserialization time: 5369 ns

gpb, serialized size: 150 bytes, avg serialization time: 9009 ns, avg deserialization time: 2148 ns
```
