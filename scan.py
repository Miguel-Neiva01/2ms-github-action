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
    os.makedirs(RESULTS_DIR, exist_ok=True)

    for repo_name in os.listdir(REPOS_DIR):
        repo_path = os.path.join(REPOS_DIR, repo_name)
        sarif_path = os.path.join(RESULTS_DIR, f"{repo_name}.sarif")

        print(f"Running 2ms scan for {repo_name}...")

        subprocess.run([
            "docker", "run",
            "-v", f"{os.getcwd()}:/repos",
            "-v", f"{os.getcwd()}/results:/results",
            "checkmarx/2ms:latest",
            "filesystem",
            "--path", f"/repos/{repo_path}",
            "--ignore-on-exit", "results",
            "--report-path", f"/results/{repo_name}.sarif"
        ], check=True)

def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.json.")
        return

    clone_repos(repos)
    run_2ms_scan()

if __name__ == "__main__":
    main()
