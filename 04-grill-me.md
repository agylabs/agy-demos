# Demo 4: /grill-me — Interactive Requirements Gathering

**Feature**: `/grill-me` makes agy interview you with targeted questions before implementing, eliminating ambiguity upfront.

## What Is /grill-me?

Instead of guessing or making assumptions, `/grill-me` triggers an interactive interview where agy asks a series of design questions — each with curated options and recommendations — before writing any code.

## Demo: URL Shortener Service

**Prompt sent to agy:**
```
/grill-me I want to build a URL shortener service
```

**Questions agy asked (with interactive TUI selectors):**

| # | Question | Options Offered | Selected |
|---|----------|----------------|----------|
| 1 | Technology stack? | Python/FastAPI+SQLite, Go+SQLite, Node/Express, Firebase | Python/FastAPI+SQLite |
| 2 | Slug generation strategy? | Random token, Auto-increment ID, Truncated hash | Secure Random Token (6-char Base62) |
| 3 | User interface type? | Web UI + API, Pure REST API, React SPA + API | Interactive Web UI + JSON API |
| 4 | Additional features? (multi-select) | Click tracking, TTL expiration, QR codes, Delete key, Passwords | Click tracking + TTL + QR codes |
| 5 | Where to build? | `url_shortener/` subdirectory, workspace root | `url_shortener/` subdirectory |

**How it looked in the TUI:**
- Single-select: `> 1. (Recommended) Python with FastAPI and SQLite` with arrow key navigation
- Multi-select: `[ ] Click Tracking` toggleable with `x` key
- Each option includes a description explaining tradeoffs

**Result**: After 5 questions, agy produced a detailed `implementation_plan.md` with full design alignment, then began building.

## Design Summary (from the interview)

- **Stack**: Python + FastAPI + SQLite
- **Slugs**: Cryptographically secure 6-char Base62 random tokens
- **UI**: Glassmorphic dark-mode SPA served by FastAPI
- **Features**: Click tracking, link expiration (TTL), QR code generation

## Key Takeaway

`/grill-me` is the opposite of `/goal` — instead of charging ahead, it pauses to gather requirements first. Use it when the task is ambiguous or has many design choices. The interactive TUI selectors make it fast and visual.
