# checking the data type
def detect_type(data: bytes) -> str:
    if not data:
        return "unknown"
    if data.startswith(b"\x89PNG"):
        return "image"
    if data.startswith(b"\xff\xd8\xff"):
        return "image"
    try:
        data.decode("utf-8")
        return "text"
    except UnicodeDecodeError:
        return "unknown"
