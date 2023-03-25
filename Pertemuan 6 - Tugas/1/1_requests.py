import requests
req = requests.get("https://classroom.its.ac.id/")
print(req.links)