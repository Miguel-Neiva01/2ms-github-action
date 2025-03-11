import os
import subprocess

REPOS_DIR = "repos"

def clone_repos(repos):
    os.makedirs(REPOS_DIR, exist_ok=True)

    for repo in repos:
        repo_name = os.path.basename(repo).replace(".git", "")
        target_dir = os.path.join(REPOS_DIR, repo_name)
        
        if os.path.exists(target_dir):
            print(f"Repository {repo_name} already cloned, pulling latest changes...")
            subprocess.run(["git", "-C", target_dir, "pull"], check=True)
        else:
            subprocess.run(["git", "clone", "--depth=1", repo, target_dir], check=True)
