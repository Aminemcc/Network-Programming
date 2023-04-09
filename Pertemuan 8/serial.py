import json

msg = ["aa", 2, [1,2,3,4,5]]
data = json.dumps(msg)
print(data)
with open("a.json", "w") as f:
    f.write(data)
