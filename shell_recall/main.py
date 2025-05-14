#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()
from shell_recall.extract import fetch_new_commands
from shell_recall.group import group_commands
from shell_recall.summarize import summarize_session
from shell_recall.write_md import write_markdown_log

import os

print("Vault path is:", os.getenv("SHELL_RECALL_VAULT"))


def is_valid_session(session):
    cmds = session.get("commands", [])
    return (
        len(cmds) > 0 and
        any("UNKNOWN" not in cmd["timestamp"] for cmd in cmds)
    )


def write_fallback_summary(session):
    print("⚠️ Writing fallback for malformed session.")
    fallback = {
        "summary": "Unstructured or malformed shell session.",
        "tags": ["meta-incomplete"],
        "start": session["commands"][0].get("timestamp", "UNKNOWN_START"),
        "end": session["commands"][-1].get("timestamp", "UNKNOWN_END"),
        "cwd": session["commands"][0].get("cwd", "UNKNOWN_DIR"),
        "commands": session["commands"],
    }
    write_markdown_log(fallback)
    print(f"Wrote fallback session from {fallback['start']} → {fallback['end']}")


def main():
    print("Fetching new commands...")
    commands = fetch_new_commands()

    if not commands:
        print("No new commands found.")
        return

    sessions = group_commands(commands)
    print(f"Found {len(sessions)} session(s)")

    for session in sessions:
        if not is_valid_session(session):
            write_fallback_summary(session)
            continue

        summary = summarize_session(session)
        if summary:
            write_markdown_log(summary)
            print(f"Wrote session from {summary.get('start', '?')} → {summary.get('end', '?')}")
        else:
            print("Skipping session: failed to summarize")


if __name__ == "__main__":
    main()
