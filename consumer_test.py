import json
from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers" : "localhost:9092",
    "group.id" : "workers",
    "auto.offset.reset" : "earliest",
    "enable.auto.commit": False,
})
consumer.subscribe(["file-upload"])

try:
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        else:
            print(msg.value())
            print("offset", msg.offset())
            consumer.commit(message=msg)
except KeyboardInterrupt:
    print("stopping")
finally:
    consumer.close()
