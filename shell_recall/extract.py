import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

ATUIN = os.getenv("SHELL_RECALL_ATUIN_PATH", "atuin")

def fetch_new_commands():
    fmt = "{time} | {directory} | {command}"
    cmd = [
        ATUIN, "search",
        "--after", "yesterday",
        "--format", fmt
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Error running Atuin:", e)
        return []

    commands = []
    last_valid_time = "UNKNOWN_TIME"
    last_valid_dir = "UNKNOWN_DIR"

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue

        parts = line.split(" | ", 2)
        if len(parts) == 3:
            ts_str, cwd, command = map(str.strip, parts)
            last_valid_time = ts_str
            last_valid_dir = cwd
        else:
            command = line.strip()
            print(f"⚠️ Malformed line. Falling back: {command}")
            ts_str = last_valid_time
            cwd = last_valid_dir

        commands.append({
            "timestamp": ts_str,
            "cwd": cwd,
            "command": command
        })

    return commands
