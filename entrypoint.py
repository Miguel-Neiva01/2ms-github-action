import os
import json
import subprocess

REPOS_DIR = "repos"
RESULTS_DIR = "results"

def load_repos():
    with open("/app/repos.json", "r") as f:
        data = json.load(f)
    return data.get("projects", [])

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

        

def run_2ms_scan():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    subprocess.run(["chmod", "-R", "777", RESULTS_DIR], check=True)

    repos_path = REPOS_DIR
 

    for repo_name in os.listdir(repos_path):
        repo_path = os.path.join(REPOS_DIR, repo_name) 
        sarif_path = os.path.join(RESULTS_DIR, f"{repo_name}.sarif")  

    

        subprocess.run([
                "/app/2ms", "filesystem",
                "--path", repo_path, 
                "--ignore-on-exit", "results",
                "--report-path", sarif_path
            ], check=True)
        
        

def merge_results():
    merged_data = {}

    # Primeiro, processa todos os ficheiros .sarif individuais e armazena os dados
    sarif_files = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".sarif"):
            file_path = os.path.join(RESULTS_DIR, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)

            repo_name = os.path.splitext(filename)[0]
            runs = data.get("runs", [])
            total_items_scanned = len(runs[0].get("results", [])) if runs else 0

            merged_data[repo_name] = {
                'total-items-scanned': total_items_scanned,
            }

            sarif_files.append(file_path)  # Armazenar os caminhos dos arquivos para remoção posterior

    
    for file_path in sarif_files:
        os.remove(file_path)

    output_file = os.path.join(RESULTS_DIR, "merged_results.sarif")
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.json.")
        return

    clone_repos(repos)
    run_2ms_scan()
    merge_results

if __name__ == "__main__":
    main()