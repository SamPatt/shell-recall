from shell_recall.extract import fetch_new_commands
from shell_recall.group import group_commands

commands = fetch_new_commands()
sessions = group_commands(commands)

for i, session in enumerate(sessions):
    print(f"\n--- Session {i+1} ({session['cwd']}) ---")
    print(f"From {session['start']} to {session['end']}")
    for cmd in session["commands"]:
        print(f"  {cmd['timestamp']}: {cmd['command']}")
