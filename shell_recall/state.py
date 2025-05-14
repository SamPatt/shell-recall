# import os
# from pathlib import Path
# from datetime import datetime

# STATE_FILE = Path.home() / ".cache" / "shell-recall" / "last_timestamp.txt"
# DEFAULT_TIMESTAMP = "2000-01-01T00:00:00Z"  # fallback for first run

# def get_last_timestamp() -> str:
#     if not STATE_FILE.exists():
#         return DEFAULT_TIMESTAMP
#     return STATE_FILE.read_text().strip()

# def set_last_timestamp(timestamp: str):
#     try:
#         ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
#         clean_ts = ts.replace(microsecond=0).isoformat().replace("+00:00", "Z")
#     except Exception:
#         clean_ts = timestamp  # fallback to raw if parsing fails
#     STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
#     STATE_FILE.write_text(clean_ts + "\n")


# def update_if_newer(new_ts: str):
#     current_ts = get_last_timestamp()
#     if new_ts > current_ts:
#         set_last_timestamp(new_ts)
