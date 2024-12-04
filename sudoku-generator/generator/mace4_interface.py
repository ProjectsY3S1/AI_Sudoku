import subprocess

def run_mace4(input_file: str):
    process = subprocess.run(
    ["/mnt/c/Personal stuff/Year 3 Sem 1/AI/LADR-2009-11A/bin/mace4", "-f", input_file],
    capture_output=True,
    text=True
    )

    return process.stdout
