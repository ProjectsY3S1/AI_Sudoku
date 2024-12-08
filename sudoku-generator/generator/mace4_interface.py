import subprocess

def run_mace4(input_file: str, output_file: str):
    with open(output_file, "w") as outfile:
        process = subprocess.run(
            ["/mnt/c/Personal stuff/Year 3 Sem 1/AI/LADR-2009-11A/bin/mace4", "-f", input_file],
            stdout=outfile,  # Redirect stdout to the file
            stderr=subprocess.PIPE,  # Capture stderr if needed
            text=True
        )
    
    if process.returncode != 0:
        # Handle errors if needed
        print(f"Error running mace4: {process.stderr}")
    
    return process.returncode
