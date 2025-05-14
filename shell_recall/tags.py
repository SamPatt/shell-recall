TAG_MAP = {
    # Projects
    "project:shellrecall": "project-shell-recall",
    "project:shell_recall": "project-shell-recall",
    "project:shell-recall": "project-shell-recall",
    "project_shell-recall": "project-shell-recall",

    # Tasks
    "task:test": "task-testing",
    "task:tests": "task-testing",
    "task:verify": "task-testing",
    "task:debug": "task-debugging",
    "task:development": "task-development",
    "task:dev": "task-development",
    "task:setup": "task-development",
    "task_development": "task-development",

    # Tools
    "tool:git": "tool-git",
    "tool:atuin": "tool-atuin",
    "tool:ollama": "tool-ollama",
    "tool_git": "tool-git",
    "tool_atuin": "tool-atuin",

    # Environment
    "env:local": "env-local",
    "env:dev": "env-local",
    "env_local": "env-local",

    # Languages
    "lang:python": "lang-python",
    "language:python": "lang-python",
    "language_python": "lang-python",
}

def normalize_tag(raw_tag):
    key = raw_tag.lower().replace(" ", "").replace("_", "-").replace(":", "-")
    return TAG_MAP.get(key, key)  # default to normalized key
