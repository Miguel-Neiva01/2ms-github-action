import json

def load_repos():
    with open("/repos.json", "r") as f:
        data = json.load(f)
    return data.get("projects", [])