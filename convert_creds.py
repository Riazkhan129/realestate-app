import json

with open("google_creds.json", "r") as f:
    data = json.load(f)
    print(json.dumps(data))
