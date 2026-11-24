import json

import psycopg
from confluent_kafka import Consumer

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "workers",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
)
consumer.subscribe(["file-upload"])

conn = psycopg.connect("host=localhost port=5432 dbname=rag user=rag password=rag")

try:
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue

        if msg.error() is not None:
            print("error:", msg.error())
            continue
        else:
            raw = msg.value()
            if raw is None:
                continue

            text = raw.decode("utf-8")
            event = json.loads(text)

            cur = conn.execute(
                "INSERT INTO files (file_id, bucket, key, content_type) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT (file_id) DO NOTHING",
                (
                    event["file_id"],
                    event["bucket"],
                    event["key"],
                    event["content_type"],
                ),
            )

            print("found file id:", event["file_id"], "and its key:", event["key"])
            conn.commit()
            consumer.commit(message=msg)

except KeyboardInterrupt:
    print("\nstopping...")

finally:
    consumer.close()
    conn.close()
