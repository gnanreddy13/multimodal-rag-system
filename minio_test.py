import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="raguser",
    aws_secret_access_key="ragpassword123",
    region_name="us-east-1",
)

try:
    s3.create_bucket(Bucket="uploads")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print("bucket already exists")

print([b["Name"] for b in s3.list_buckets()["Buckets"]])

data = b"hello from minio"
s3.put_object(Bucket="uploads", Key="test.txt", Body=data)

response = s3.get_object(Bucket="uploads", Key="test.txt")
back = response["Body"].read()
print(back)
print(back == data)
