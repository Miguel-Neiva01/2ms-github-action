import os
import subprocess
import time

def run_2ms_scan(REPOS_DIR, RESULTS_DIR):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    subprocess.run(["chmod", "-R", "777", RESULTS_DIR], check=True)

    repo_scan_results = {}

    for repo_name in os.listdir(REPOS_DIR):
        repo_path = os.path.join(REPOS_DIR, repo_name) 
        sarif_path = os.path.join(RESULTS_DIR, f"{repo_name}.sarif")  

        print(f"Starting scan for {repo_name}...")

        start_time = time.time()  

        try:
            subprocess.run([
                "/tmp/2ms", "filesystem",
                "--path", repo_path, 
                "--ignore-on-exit", "results",
                "--report-path", sarif_path
            ], check=True)
            success = True  
        except subprocess.CalledProcessError as e:
            print(f"2ms scan failed for {repo_name}. Error: {e}. Marking test as failed.")
            success = False  

        end_time = time.time()  
        duration = round(end_time - start_time, 3) 

        repo_scan_results[repo_name] = {
            "scan_status": success,
            "execution_time": duration
        }

    return repo_scan_results
