import subprocess
import json
import re
from shell_recall.tags import normalize_tag
import os

DEFAULT_MODEL = os.getenv("SHELL_RECALL_MODEL", "qwq:32b")

def call_ollama(prompt: str, model: str = DEFAULT_MODEL):

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error calling Ollama:", e)
        return ""


def build_prompt(session):
    lines = [f"[{cmd['timestamp']}] {cmd['command']}" for cmd in session["commands"]]
    joined = "\n".join(lines)

    return f"""You are a system summarizer. Given a list of shell commands in a time-ordered session, produce:

1. A concise natural language summary of what was being done
2. A list of 3–6 relevant tags using only lowercase words and **hyphens** (e.g. 'project-x', 'task-debugging', 'tool-y', 'env-local'). Avoid colons, underscores, or spaces. If the commands are related to a code base, create a project tag based on the name of the code repository.

Commands:
{joined}

Respond with ONLY this raw JSON object and no commentary or markdown code blocks:
{{"summary": "...", "tags": ["project-x-y", "task-debugging"]}}
"""


def summarize_session(session, model=DEFAULT_MODEL):
    prompt = build_prompt(session)
    response = call_ollama(prompt, model)

    if not session["commands"]:
        print("⚠️ Empty command list, skipping LLM call.")
        return None

    # Extract first valid JSON object using regex
    match = re.search(r'\{.*?\}', response, re.DOTALL)
    if not match:
        print("Could not find JSON object in LLM output:")
        print(response)
        return None

    try:
        parsed = json.loads(match.group(0))

        raw_tags = parsed.get("tags", [])
        normalized_tags = [normalize_tag(tag) for tag in raw_tags]

        return {
            "summary": parsed.get("summary", ""),
            "tags": normalized_tags,
            "start": session["start"],
            "end": session["end"],
            "cwd": session["cwd"],
            "commands": session["commands"]
        }
    except json.JSONDecodeError:
        print("Could not parse JSON from LLM output:")
        print(match.group(0))
        return None
