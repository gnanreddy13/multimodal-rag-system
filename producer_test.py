import json
from confluent_kafka import Producer

def report(err, msg):
    if err is not None:
        print("error:", err)
    else:
        print("delivered to", msg.topic(), "partition", msg.partition(), "offset", msg.offset())

producer = Producer({"bootstrap.servers" : "localhost:9092"})
event = {"file_id": "a1b2c3", "bucket": "uploads", "key": "a1b2c3.png", "content_type": "image/png"}

producer.produce("file-upload", key = event["file_id"], value = json.dumps(event).encode("utf-8"), on_delivery = report)
producer.flush()

print("flush done")
