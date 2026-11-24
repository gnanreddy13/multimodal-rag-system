import psycopg

event = {
    "file_id": "image3",
    "bucket": "uploads",
    "key": "image3.png",
    "content_type": "image/png",
}

conn = psycopg.connect("host=localhost port=5432 dbname=rag user=rag password=rag")
cur = conn.execute(
    "INSERT INTO files (file_id, bucket, key, content_type) "
    "VALUES (%s, %s, %s, %s) ON CONFLICT (file_id) DO NOTHING",
    (event["file_id"], event["bucket"], event["key"], event["content_type"]),
)
conn.commit()
print("inserted rows:", cur.rowcount)
conn.close()
