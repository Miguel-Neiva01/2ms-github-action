import os
import json

def merge_results(repo_scan_results, RESULTS_DIR):
    merged_data = {}

    json_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".json")]
    print(f"JSON files found: {json_files}")

    for filename in json_files:
        file_path = os.path.join(RESULTS_DIR, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {file_path}")
                    continue

            repo_name = os.path.splitext(filename)[0]
            runs = data.get("runs", [])
            total_items_scanned = len(runs[0].get("results", [])) if runs else 0
            repo_scan = repo_scan_results.get(repo_name, False)

            merged_data[repo_name] = {
                'total-items-scanned': total_items_scanned,
                'repo_scan': repo_scan,
            }

    output_file = os.path.join(RESULTS_DIR, "results.json")
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)
