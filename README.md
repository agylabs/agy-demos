# AGY CLI Feature Demos

> **[View the interactive slide deck and full docs](https://agylabs.github.io/agy-demos/)** — the best way to explore these demos.

Bite-sized demos showcasing [Antigravity CLI](https://antigravity.google) (`agy`) features. Each demo highlights a different capability with real prompts, real outputs, and working sample code.

- [Slides](https://agylabs.github.io/agy-demos/) — Quick visual overview of all 8 features
- [Docs](https://agylabs.github.io/agy-demos/guide.html) — Detailed walkthrough for each demo

## Prerequisites

- [Antigravity CLI](https://antigravity.google) installed (`agy`)
- Enterprise auth configured (recommended) or Google OAuth
- Model set to `Gemini 3.5 Flash` (via `/model` in interactive mode)

## Demos

| # | Feature | File | Description |
|---|---------|------|-------------|
| 1 | Skills | [01-skills.md](01-skills.md) | List and run built-in skills (56+ available) |
| 2 | Subagents | [02-subagents.md](02-subagents.md) | Spawn background research agents for parallel work |
| 3 | /goal | [03-goal.md](03-goal.md) | Autonomous task completion — plan, build, test, verify |
| 4 | /grill-me | [04-grill-me.md](04-grill-me.md) | Interactive requirements gathering with TUI selectors |
| 5 | /schedule | [05-schedule.md](05-schedule.md) | Recurring and one-shot scheduled tasks |
| 6 | Web Browsing | [06-web-browsing.md](06-web-browsing.md) | Fetch and use live web content |
| 7 | Workflow Skills | [07-workflow-skill.md](07-workflow-skill.md) | Distill workflows into reusable skills |
| 8 | Image Generation | [08-image-gen.md](08-image-gen.md) | Generate images and assets with text-to-image |

## Sample Artifacts

These artifacts were created by agy during the demos:

| Artifact | Created During | Description |
|----------|---------------|-------------|
| `countdown.py` + `test_countdown.py` | Demo 3 (/goal) | Python CLI tool with 9 passing tests |
| `url_shortener/` | Demo 4 (/grill-me) | Full FastAPI + SQLite app with glassmorphic UI |
| `task_manager/` | Demo 7 (Workflow Skill) | Validation app scaffolded by the custom skill |
| `go-news.md` | Demo 2 (Subagents) | Go 1.24 research by a background subagent |
| `gemini-flash-notes.md` | Demo 6 (Web Browsing) | Live web research results |
| `rocket-launch.png` | Demo 8 (Image Gen) | AI-generated image |

## Running the Sample Apps

```bash
# URL Shortener (from Demo 4)
cd url_shortener
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000

# Task Manager (from Demo 7)
cd task_manager
pip install fastapi uvicorn
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
# Open http://localhost:8001

# Countdown CLI (from Demo 3)
python3 countdown.py 10
python3 countdown.py 5 --reverse
python3 -m unittest test_countdown.py
```

## License

Apache 2.0
