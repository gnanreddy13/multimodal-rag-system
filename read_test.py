from detect import detect_type

with open("samples/black.jpg", "rb") as f:
    data = f.read()

print(type(data))
print(len(data))
print(detect_type(data))
