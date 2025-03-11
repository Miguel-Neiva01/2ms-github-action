from src.clone import clone_repos
from src.scan import run_2ms_scan
from src.merge import merge_results
from src.node_script import run_node_script
from src.load_repos import load_repos
import os

RESULTS_DIR = "results"
REPOS_DIR = "repos"

def main():
    repos = load_repos()
    if not repos:
        print("No repositories found in repos.json.")
        return

    clone_repos(repos)
    repo_scan_results = run_2ms_scan(REPOS_DIR, RESULTS_DIR)
    merge_results(repo_scan_results, RESULTS_DIR)
    run_node_script()

    results_remove = os.path.join(RESULTS_DIR, "results.json")
    if os.path.exists(results_remove):
        os.remove(results_remove)

if __name__ == "__main__":
    main()
