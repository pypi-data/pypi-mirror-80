from pulsar.schema import (
    Record,
    String,
    Array,
    Float,
)


class TextSchema(Record):
    uuid = String(required=True)
    text = String()
    sequence_id = String()


class TextEmbeddingSchema(Record):
    uuid = String(required=True)
    text = String()
    embedding = Array(Float())
