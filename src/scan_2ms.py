import os
import subprocess

def run_2ms_scan(REPOS_DIR, RESULTS_DIR):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    subprocess.run(["chmod", "-R", "777", RESULTS_DIR], check=True)

    repo_scan_results = {}

    for repo_name in os.listdir(REPOS_DIR):
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
            
    print(f"Scan results: {repo_scan_results}")
    return repo_scan_results
