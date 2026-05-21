# Demo 7: Workflow Skill Creator

**Feature**: Distill any completed workflow into a reusable, shareable skill that agy can invoke in future sessions.

## What Is the Workflow Skill Creator?

After completing a complex multi-step workflow (like building a FastAPI app), agy can analyze what it did and create a reusable **SKILL.md** file — a structured protocol that guides future agy sessions to reproduce the same workflow pattern with different inputs.

## Demo: Creating "fastapi-app-scaffold" Skill

**Prompt sent to agy:**
```
Use the workflow-skill-creator skill to distill our URL shortener building workflow into
a reusable skill called "fastapi-app-scaffold" that can scaffold any FastAPI + SQLite
web application with tests.
```

**What agy did (structured brainstorming process):**

| Phase | Action |
|-------|--------|
| **Phase 1: Brainstorming** | Asked 6 clarifying questions across 2 rounds |
| Round 1 | Workflow accuracy, input format, usage frequency |
| Round 2 | Error handling strategy, database layer, skill pattern |
| **Phase 2: Design** | Created `implementation_plan.md` artifact |
| **Phase 3: Implementation** | Wrote `SKILL.md` with full protocol |
| **Phase 4: Validation** | Scaffolded a "Task Manager" app using the new skill |
| **Phase 5: Self-Healing** | Fixed namespace collision, re-ran tests (7/7 passed) |

**Decisions captured in the skill:**
- API-only or API+Frontend (configurable)
- Natural language input for requirements
- Raw sqlite3 by default, ORM if specified
- Self-healing test verification loop
- Modern CSS glassmorphism for frontends

## Skill File Created

```
.gemini/skills/fastapi-app-scaffold/SKILL.md
```

**Future usage**: Simply say "Use the fastapi-app-scaffold skill to scaffold a blog API" and agy follows the entire protocol automatically.

## Validation App Created

Agy validated the skill by building a complete **Task Manager** app:
```
task_manager/
├── app/
│   ├── main.py          # FastAPI CRUD endpoints
│   ├── database.py      # SQLite with parameterized queries
│   ├── schemas.py       # Pydantic validation
│   └── static/          # Glassmorphic dark-mode frontend
├── tests/
│   └── test_main.py     # 7 integration tests (all passing)
└── requirements.txt
```

## Key Takeaway

The workflow skill creator turns one-off work into institutional knowledge. Build something once, distill it into a skill, and agy can reproduce the pattern indefinitely — with full self-healing and validation built in.
