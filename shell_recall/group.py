from datetime import datetime, timedelta
from pathlib import Path

def parse_timestamp(ts):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None

def dirs_related(dir1, dir2, depth=2):
    try:
        path1 = Path(dir1).resolve()
        path2 = Path(dir2).resolve()

        # One is subdir of the other
        if path1 in path2.parents or path2 in path1.parents:
            return True

        # Share a common prefix up to N levels
        parts1 = path1.parts[:depth]
        parts2 = path2.parts[:depth]
        return parts1 == parts2
    except Exception:
        return False  # fallback if parsing fails

def group_commands(commands, max_gap_minutes=20, dir_depth=2):
    sessions = []
    current_session = None
    max_gap = timedelta(minutes=max_gap_minutes)

    for entry in sorted(commands, key=lambda x: parse_timestamp(x["timestamp"]) or datetime.min):
        ts = parse_timestamp(entry["timestamp"])

        if current_session is None:
            current_session = {
                "start": entry["timestamp"],
                "end": entry["timestamp"],
                "cwd": entry["cwd"],
                "commands": [entry]
            }
            continue

        prev_ts = parse_timestamp(current_session["end"])
        same_project_area = dirs_related(entry["cwd"], current_session["cwd"], dir_depth)
        time_close = ts and prev_ts and (ts - prev_ts) <= max_gap

        if same_project_area and time_close:
            current_session["commands"].append(entry)
            current_session["end"] = entry["timestamp"]
        else:
            sessions.append(current_session)
            current_session = {
                "start": entry["timestamp"],
                "end": entry["timestamp"],
                "cwd": entry["cwd"],
                "commands": [entry]
            }

    if current_session:
        sessions.append(current_session)

    return sessions
