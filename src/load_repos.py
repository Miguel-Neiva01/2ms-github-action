import json
import os

def load_repos():
    repos_file = "/app/repos.sarif"

    try:
       
        with open(repos_file, "r") as f:
            data = json.load(f)


        projects = []
        if "runs" in data:
            for run in data["runs"]:
                for artifact in run.get("artifacts", []):
                    projects.append(artifact.get("name", ""))
        
        return projects

    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo SARIF. O formato pode estar incorreto.")
        return []
    except FileNotFoundError:
        print(f"O arquivo {repos_file} não foi encontrado.")
        return []
