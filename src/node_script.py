import subprocess
def run_node_script():
    print("Executing node script...")
    try:
        subprocess.run(["node", "/app/create_summary/main.js"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
