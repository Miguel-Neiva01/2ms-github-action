import json

def load_repos():
    with open("/app/repos.json", "r") as f:
        data = json.load(f)
    return data.get("projects", [])