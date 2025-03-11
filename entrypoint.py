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
    repo_scan_results= {}

    for repo_name in os.listdir(repos_path):
        repo_path = os.path.join(REPOS_DIR, repo_name) 
        json_path = os.path.join(RESULTS_DIR, f"{repo_name}.json")  

        try:
            subprocess.run([
                "/app/2ms", "filesystem",
                "--path", repo_path, 
                "--ignore-on-exit", "results",
                "--report-path", json_path
            ], check=True)
            repo_scan_results[repo_name] = True  
        except subprocess.CalledProcessError:
            print(f"2ms scan failed for {repo_name}. Marking test as failed.")
            repo_scan_results[repo_name] = False 
            
    return repo_scan_results

        

def merge_results(repo_scan_results):
    merged_data = {}

    json_files = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(RESULTS_DIR, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)

            repo_name = os.path.splitext(filename)[0]
            runs = data.get("runs", [])
            total_items_scanned = len(runs[0].get("results", [])) if runs else 0
            repo_scan= repo_scan_results.get(repo_name,False)

            merged_data[repo_name] = {
                'total-items-scanned': total_items_scanned,
                'repo_scan' : repo_scan,
            }

            json_files.append(file_path) 


    output_file = os.path.join(RESULTS_DIR, "results.json")
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

def run_node_script():
    print("Execute node script")
    try:
        subprocess.run(["node", "/app/src/main.js"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.json.")
        return

    clone_repos(repos)

    repo_scan_results = run_2ms_scan()

    merge_results(repo_scan_results)

    run_node_script()

    
    results_json_path = os.path.join(RESULTS_DIR, "results.json")
    if os.path.exists(results_json_path):
        os.remove(results_json_path)


if __name__ == "__main__":
    main()