import os
import json

def merge_results(repo_scan_results, RESULTS_DIR):
    merged_data = {}

    sarif_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".sarif")]
    print(f"SARIF files found: {sarif_files}")

    for filename in sarif_files:
        file_path = os.path.join(RESULTS_DIR, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)  
                except json.JSONDecodeError:
                    print(f"Skipping invalid SARIF file: {file_path}")
                    continue

            repo_name = os.path.splitext(filename)[0]

       
            total_items_scanned = data.get("runs", [{}])[0].get("tool", {}).get("driver", {}).get("name", "Unknown")
            total_secrets_found = len(data.get("runs", [{}])[0].get("results", []))
            repo_scan = repo_scan_results.get(repo_name, False)

            merged_data[repo_name] = {
                'total-items-scanned': total_items_scanned,
                'total-secrets-found': total_secrets_found,
                'repo_scan': repo_scan,
            }

    # Gravar os resultados no arquivo final
    output_file = os.path.join(RESULTS_DIR, "results.sarif")
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)
    print(f"Results saved to {output_file}")
