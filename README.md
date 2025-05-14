# shell-recall

`shell-recall` is a Python tool that turns your shell history into organized, LLM-summarized daily logs — complete with natural language summaries, tags, and visual structure for Obsidian.

It’s built to help you:

- Remember what you were doing
- Track work across sessions and projects
- Create a searchable terminal journal with zero manual effort

---

## 🧠 How It Works

1. **Fetches recent shell commands** using [Atuin](https://atuin.sh)
2. **Groups** them into sessions (by directory + time proximity)
3. **Summarizes** each session using a local LLM via [Ollama](https://ollama.ai)
4. **Writes** a Markdown log to your Obsidian vault (one file per day)

Example output:

```markdown
## 2025-05-14T12:15:38 → 2025-05-14T12:16:24
**Directory**: `/home/user/code`  
**Tags**: #project-mytool #task-debugging #env-local #tool-git  

**Summary**:  
Initialized a new git repository and committed the project skeleton.

<details>
<summary>Commands</summary>

- `git init`
- `touch README.md`
- `git add .`
- `git commit -m "initial commit"`

</details>
```

---

## 📦 Project Structure

```
shell-recall/
├── shell_recall/
│   ├── extract.py         # Fetches new shell commands via Atuin
│   ├── group.py           # Groups commands into sessions by time + directory
│   ├── summarize.py       # Calls Ollama to generate summaries and tags
│   ├── write_md.py        # Writes formatted Markdown into your Obsidian vault
│   ├── tags.py            # Tag normalization and canonical mapping
│   ├── main.py            # Entrypoint: pulls, groups, summarizes, and writes
│   ├── state.py           # (Commented out) Timestamp tracking logic for incremental fetch
├── .env                   # Local config: vault path, model name
├── test_*.py              # One-off scripts to test each component
```

---

## ⚙️ Setup

### 1. Install Dependencies
It's currently only using `python-dotenv`

```bash
pip install -r requirements.txt
# You'll also need Atuin and Ollama installed
```

### 2. Create a `.env` file

```env
SHELL_RECALL_VAULT=/absolute/path/to/your/obsidian/vault/terminal-journal
SHELL_RECALL_MODEL=your-ollama-model-name
SHELL_RECALL_ATUIN_PATH=/absolute/path/to/ATUIN
```

### 3. Initialize Atuin

Follow setup at [atuin.sh](https://docs.atuin.sh) — make sure you can run:

```bash
atuin search --after "yesterday"
```

---

## 🚀 Run It

### Manual
```bash
python3 -m shell_recall.main
```

This will:
- Pull all commands since **yesterday**
- Group + summarize them
- Append them to the correct Markdown file in your vault

### Automated

If you want this to run daily without manual intervention, you can set it up using either:

    systemd (recommended for desktop Linux users)

    cron (simple for server environments)

Automation setup is optional and not required to use the tool.

---

## 🛠 Notes

- `state.py` and `test_state.py` are currently **commented out**. They contain timestamp tracking logic, but were paused due to Atuin's `--after` not filtering strictly.
- Right now we use `--after "yesterday"` and filter client-side.
- Malformed or incomplete sessions are still included, tagged `#meta-incomplete`.

---

## 🧭 Roadmap Ideas

- ✅ Tag normalization (`tag-map`) to keep Obsidian tagging consistent
- ⏳ Restore strict timestamp state tracking once Atuin filtering improves
- 📊 Web-based timeline UI
- 🔁 Duplicate session detection
- 🔄 Git integration for log syncing

---

## 🧵 Author

Built by [Sam Patt](https://github.com/SamPatt) — originally to track his own development and project work across a busy terminal history.

PRs and feedback welcome.
