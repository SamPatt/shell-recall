from shell_recall.extract import fetch_new_commands
from shell_recall.group import group_commands
from shell_recall.summarize import summarize_session
from shell_recall.write_md import write_markdown_log

commands = fetch_new_commands()
sessions = group_commands(commands)

if sessions:
    summary = summarize_session(sessions[-1])
    if summary:
        write_markdown_log(summary)
        print("Markdown log updated!")
else:
    print("No sessions found.")
