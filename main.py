import json
from src.clone_repos import clone_repos
from src.scan_2ms import run_2ms_scan
from src.merge_results import merge_results
from src.node_script import run_node_script
from src.load_repos import load_repos
import os

RESULTS_DIR = "/app/results"
REPOS_DIR = "/app/repos"

def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.sarif.")

    clone_repos(repos)
    repo_scan_results = run_2ms_scan(REPOS_DIR, RESULTS_DIR)
    merge_results(repo_scan_results, RESULTS_DIR)
    run_node_script()

    results_path = os.path.join(RESULTS_DIR, "results.sarif")
    

    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            os.remove(results_path)

if __name__ == "__main__":
    main()
