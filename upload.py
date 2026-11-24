import json
import uuid

import boto3
from confluent_kafka import Producer

from detect import detect_type


# to verify if msg was delivered or not
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


# initialize obj storage & producer
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="raguser",
    aws_secret_access_key="ragpassword123",
    region_name="us-east-1",
)
producer = Producer({"bootstrap.servers": "localhost:9092"})

# opens a file from a dir
with open("samples/black.jpg", "rb") as f:
    data = f.read()

# init an upload id for the file
file_id = str(uuid.uuid4())

# store the obj
s3.put_object(Bucket="uploads", Key=file_id, Body=data)

# publish the note to kafka
event = {
    "file_id": file_id,
    "bucket": "uploads",
    "key": file_id,
    "content_type": detect_type(data),
}
producer.produce(
    topic="file-upload",
    key=file_id,
    value=json.dumps(event).encode("utf-8"),
    on_delivery=report,
)

# wait until uploading is finished
producer.flush()
print("stored and announced", file_id)
