import os
import json
import subprocess

REPOS_DIR = "repos"
RESULTS_DIR = "results"

def load_repos():
    with open("repos.json", "r") as f:
        data = json.load(f)
    return data.get("projects", [])

def clone_repos(repos):
    os.makedirs(REPOS_DIR, exist_ok=True)

    for repo in repos:
        repo_name = os.path.basename(repo).replace(".git", "")
        target_dir = os.path.join(REPOS_DIR, repo_name)

        if os.path.exists(target_dir):
            print(f"Repository {repo_name} already cloned, skipping...")
            continue

        print(f"Cloning {repo} into {target_dir}")
        subprocess.run(["git", "clone", "--depth=1", repo, target_dir], check=True)

def run_2ms_scan():
    """Executa o 2ms scan e guarda os resultados localmente."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    workspace = os.getcwd()  # Garante que estamos no diretório correto
    repos_path = os.path.join(workspace, REPOS_DIR)
    results_path = os.path.join(workspace, RESULTS_DIR)

    for repo_name in os.listdir(repos_path):
        repo_path = os.path.join("/repos", repo_name)  # Caminho dentro do container
        sarif_path = os.path.join("/results", f"{repo_name}.sarif")  # Caminho dentro do container

        print(f"🔍 A correr 2ms scan para {repo_name}...")
        print(f"📂 Diretório local dos resultados: {results_path}")
        print(f"📁 Diretório montado no container: /results")

        try:
            subprocess.run([
                "docker", "run",
                "--rm",
                "-v", f"{repos_path}:/repos",
                "-v", f"{results_path}:/results",
                "checkmarx/2ms:latest",
                "filesystem",
                "--path", repo_path,  # Corrigido para não duplicar "repos/"
                "--ignore-on-exit", "results",
                "--report-path", sarif_path
            ], check=True)

            # Verificar se o relatório foi criado
            local_sarif_path = os.path.join(results_path, f"{repo_name}.sarif")
            if os.path.exists(local_sarif_path):
                print(f"✅ Relatório guardado: {local_sarif_path}")
            else:
                print(f"❌ ERRO: O relatório {repo_name}.sarif não foi criado!")

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao correr scan para {repo_name}: {e}")
            continue

def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.json.")
        return

    clone_repos(repos)
    run_2ms_scan()

if __name__ == "__main__":
    main()
