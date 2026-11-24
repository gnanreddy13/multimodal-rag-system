import json

from confluent_kafka import Producer


def report(err, msg):
    if err is not None:
        print("error:", err)
    else:
        print(
            "msg delivered to",
            msg.topic(),
            "partition",
            msg.partition(),
            "offset",
            msg.offset(),
        )


producer = Producer({"bootstrap.servers": "localhost:9092"})

event = {
    "file_id": "image4",
    "bucket": "uploads",
    "key": "image4.png",
    "content_type": "image/png",
}

text = json.dumps(event)
data = text.encode("utf-8")

producer.produce(
    topic="file-upload",
    key=event["file_id"],
    value=data,
    on_delivery=report,
)

producer.flush()
print("flush done")
