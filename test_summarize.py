from shell_recall.extract import fetch_new_commands
from shell_recall.group import group_commands
from shell_recall.summarize import summarize_session

commands = fetch_new_commands()
sessions = group_commands(commands)

if sessions:
    result = summarize_session(sessions[-1])  # Just summarize the most recent session
    print("\n--- SUMMARY ---")
    print(result["summary"])
    print("\n--- TAGS ---")
    print(result["tags"])
else:
    print("No sessions found.")
