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

    subprocess.run(["chmod", "-R", "777", RESULTS_DIR], check=True)

    workspace = os.getcwd()  
    repos_path = os.path.join(workspace, REPOS_DIR)
    results_path = os.path.join(workspace, RESULTS_DIR)

    for repo_name in os.listdir(repos_path):
        repo_path = os.path.join("/repos", repo_name)  
        sarif_path = os.path.join("/results", f"{repo_name}.sarif")  

        print(f"🔍 Runnig {repo_name}...")


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
        
def merge_results():

    results_path = "results"
    
    merged_data = {}


    for filename in os.listdir(results_path):
        if filename.endswith(".sarif"):
         
            file_path = os.path.join(results_path, filename)
            
         
            with open(file_path, 'r') as f:
                data = json.load(f)

        
            repo_name = os.path.splitext(filename)[0]

            
            total_items_scanned = data.get('tool', {}).get('driver', {}).get('properties', {}).get('total-items-scanned', 0)
            secrets = []  # Aqui você pode extrair as informações sobre "secrets" ou outros dados relevantes

            merged_data[repo_name] = {
                'total-items-scanned': total_items_scanned,
                'secrets': secrets
            }


    output_file = "merged_results.json"
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)  

           
def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.json.")
        return

    clone_repos(repos)
    run_2ms_scan()
    merge_results()

if __name__ == "__main__":
    main()
