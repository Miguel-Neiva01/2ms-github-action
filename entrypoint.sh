#!/bin/bash

REPOS_DIR="repos"
RESULTS_DIR="results"

# Função para carregar os repositórios do arquivo JSON
load_repos() {
    repos=$(jq -r '.projects[]' /app/repos.json)
    echo "$repos"
}

# Função para clonar os repositórios
clone_repos() {
    mkdir -p "$REPOS_DIR"

    for repo in $repos; do
        repo_name=$(basename "$repo" .git)
        target_dir="$REPOS_DIR/$repo_name"

        if [ -d "$target_dir" ]; then
            echo "Repository $repo_name already cloned, skipping..."
            continue
        fi

        echo "Cloning $repo into $target_dir"
        git clone --depth=1 "$repo" "$target_dir"
    done
}

# Função para rodar o scan 2ms
run_2ms_scan() {
    mkdir -p "$RESULTS_DIR"
    chmod -R 777 "$RESULTS_DIR"

    workspace=$(pwd)
    repos_path="$workspace/$REPOS_DIR"
    results_path="$workspace/$RESULTS_DIR"

    for repo_name in $(ls "$repos_path"); do
        repo_path="/repos/$repo_name"
        sarif_path="/results/$repo_name.sarif"

        echo "Running $repo_name..."
        /app/2ms filesystem --path "$repo_path" --ignore-on-exit results --report-path "$sarif_path"
    done
}

# Função para mesclar os resultados dos scans
merge_results() {
    merged_data="{}"

    for filename in $(ls "$RESULTS_DIR"); do
        if [[ "$filename" == *.sarif ]]; then
            file_path="$RESULTS_DIR/$filename"
            data=$(cat "$file_path")
            repo_name=$(basename "$filename" .sarif)
            total_items_scanned=$(echo "$data" | jq '.runs[0].results | length')

            merged_data=$(echo "$merged_data" | jq --arg repo_name "$repo_name" --argjson total_items_scanned "$total_items_scanned" \
                '. + {($repo_name): {"total-items-scanned": $total_items_scanned}}')

            rm "$file_path"
        fi
    done

    output_file="$RESULTS_DIR/merged_results.sarif"
    echo "$merged_data" | jq . > "$output_file"
}

# Função principal
main() {
    repos=$(load_repos)
    if [ -z "$repos" ]; then
        echo "No repositories found in repos.json."
        return
    fi

    clone_repos
    run_2ms_scan
    merge_results
}

main
