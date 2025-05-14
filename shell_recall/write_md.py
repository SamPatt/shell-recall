from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

import re
import os
load_dotenv()

VAULT_PATH = Path(os.getenv("SHELL_RECALL_VAULT", Path.home() / "terminal-journal"))

def sanitize_timestamp(ts):
    # If it's a proper ISO timestamp, return it
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).isoformat().replace("+00:00", "Z")
    except Exception:
        return "UNKNOWN_TIME"

def write_markdown_log(session_summary):
    session_date = session_summary["start"][:10] if "start" in session_summary else "UNKNOWN"
    filename = VAULT_PATH / f"{session_date}.md"
    VAULT_PATH.mkdir(parents=True, exist_ok=True)

    start = sanitize_timestamp(session_summary.get("start", "UNKNOWN"))
    end = sanitize_timestamp(session_summary.get("end", "UNKNOWN"))
    cwd = session_summary.get("cwd", "UNKNOWN_DIR")

    summary = session_summary.get("summary", "No summary.")
    tags = " ".join(f"#{tag.replace(':', '-').replace('_', '-')}" for tag in session_summary.get("tags", []))

    commands = session_summary.get("commands", [])
    formatted_cmds = "\n".join(f"- `{cmd.get('command', '').strip()}`" for cmd in commands)

    block = f"""
## {start} → {end}
**Directory**: `{cwd}`  
**Tags**: {tags}  

**Summary**:  
{summary}

<details>
<summary>Commands</summary>

{formatted_cmds}

</details>
"""

    print(f"Writing session to {filename}")
    with open(filename, "a") as f:
        f.write(block.strip() + "\n\n")
