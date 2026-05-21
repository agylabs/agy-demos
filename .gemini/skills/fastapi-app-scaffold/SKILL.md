---
name: fastapi-app-scaffold
description: >-
  Rapidly scaffolds high-quality, fully tested FastAPI + SQLite applications with database logic, schemas, endpoints, and an optional premium frontend.
---

# FastAPI + SQLite App Scaffolder

## Overview
This skill provides a highly disciplined, premium blueprint for scaffolding FastAPI web applications backed by a SQLite database. It covers database connection pooling, timezone-aware datetimes, Pydantic validation, CORS, error handling, clean REST endpoints, testing, and an optional high-end glassmorphic frontend UI.

---

## Dependencies
*   **modern-web-guidance**: Mandatory dependency when the optional frontend user interface is selected. Enforces modern CSS styling, HSL colors, responsive grids, and visual transitions. Install via `agy plugin install modern-web-guidance-plugin`.

---

## Quick Start
To trigger this skill, ask the agent to scaffold a FastAPI app by providing a natural-language description of your models and endpoints:

> "Use the `fastapi-app-scaffold` skill to scaffold a FastAPI application for a **Task Manager**.
> 
> *   **Models**: Task (id, title, description, is_completed, created_at, updated_at).
> *   **Endpoints**: Create task, list tasks, toggle completion, delete task.
> *   **Frontend**: Include a modern glassmorphic web UI to manage tasks.
> *   **Location**: Scaffold inside the `task_manager/` directory."

---

## Workflow

When triggered, follow these phases step-by-step to build, verify, and deliver the app.

### Phase 1: Parse and Plan
1.  **Analyze requirements**: Map the user's natural language request to a explicit database schema, database tables, Pydantic models, and REST endpoints.
2.  **Determine UI choice**: Check if the user requested a frontend. If yes, prepare to build dynamic static pages under `/static`.
3.  **Confirm Target Location**: Ensure all generated files are located strictly within the user-specified directory (e.g., `my_app/`).

### Phase 2: Database Layer (`database.py`)
1.  **SQLite Connection**: Implement a robust, thread-safe SQLite connection module. Use context managers (`contextlib.contextmanager`) to guarantee connections are closed, preventing database locks.
2.  **Raw SQLite Standard**: Unless the user explicitly requested an ORM (like SQLAlchemy or SQLModel), use raw parameterized SQL queries with `sqlite3` to ensure a zero-dependency database layer:
    ```python
    import sqlite3
    from contextlib import contextmanager

    DB_PATH = "app.db"

    @contextmanager
    def get_db():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enables dict-like access
        try:
            yield conn
        finally:
            conn.close()
    ```
3.  **Timezone-Aware Dates**: Always store datetimes as UTC strings or floats. When generating timestamps in Python, **NEVER use `datetime.utcnow()`** (deprecated in Python 3.12+). Instead, use timezone-aware UTC datetimes:
    ```python
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    ```

### Phase 3: Pydantic Schemas (`schemas.py`)
1.  Create separate request (`BaseModel` / `Create` / `Update`) and response models for each entity.
2.  Add proper type hints and Field validations (e.g., `Field(..., min_length=1)`).
3.  Ensure timestamps and foreign keys are explicitly type-hinted and documented.

### Phase 4: FastAPI Web Server (`main.py`)
1.  **Lifespan Events**: Use modern `@asynccontextmanager` `lifespan` to handle database initialization (e.g. creating tables if they do not exist). **Avoid using deprecated `@app.on_event("startup")`**:
    ```python
    from fastapi import FastAPI
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db()  # Create tables
        yield
        # Clean up if needed

    app = FastAPI(lifespan=lifespan)
    ```
2.  **CORS Middleware**: Always include `CORSMiddleware` to allow seamless local and frontend interaction:
    ```python
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```
3.  **REST Endpoints**: Expose standard REST verbs (`GET`, `POST`, `PUT`, `DELETE`). Always parameterize SQL parameters explicitly; never concatenate strings to prevent SQL injections.
4.  **Static Asset Hosting**: Mount the `/static` directory for the optional frontend:
    ```python
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
    ```

### Phase 5: Optional Frontend Assets (Inside `static/`)
If a frontend was requested, consult the `modern-web-guidance` skill and design a gorgeous Single Page App (SPA) comprising:
1.  `index.html`: Modern, semantic structure with descriptive element IDs.
2.  `style.css`: Gorgeous CSS utilizing a premium, curated dark HSL palette, smooth gradients, subtle backdrop-filters, custom glowing input borders, and responsive grid layouts.
3.  `app.js`: Clean asynchronous logic using `fetch()` to handle data submission, dynamic UI list rendering, loading states, and elegant toast/error messages.

### Phase 6: Automated Testing (`tests/test_main.py`)
Build a comprehensive suite of unit/integration tests to verify correctness:
1.  Use Python's standard `unittest` framework and `fastapi.testclient.TestClient`. This ensures a zero-dependency testing pipeline with no external `pytest` installations required.
2.  **Isolate Databases**: Use a temporary database file (e.g., `test_app.db`) for running tests, and ensure it is cleaned up/deleted in the `setUp` / `tearDown` phases.
3.  **Validate Core Flows**: Add test cases covering success scenarios, validation errors, bad payloads, and resource-not-found handling.

### Phase 7: Verification & Self-Healing
Verify the build automatically:
1.  Execute the test suite in the target directory using a clean python run command:
    ```bash
    python3 -m unittest tests/test_main.py
    ```
2.  **Analyze Outputs**: If any tests fail, inspect the error output or traceback.
3.  **Self-Correction**:
    *   Identify the bug (e.g., SQLite row formatting, JSON serialization of timezone-aware datetimes, schema field mismatch, file-locking, or directory pathing).
    *   Directly fix the code file using your editing tools.
    *   Re-run the tests.
    *   **Loop** until all tests pass completely. Do not stop or ask the user for help unless the requirement itself is logically contradictory.

---

## Common Mistakes to Avoid
*   **Naive Datetimes**: Avoid using `datetime.now()` without a timezone parameter, or deprecated methods like `datetime.utcnow()`. This causes discrepancies when comparing times.
*   **Database Lock Contention**: Failing to close a cursor or sqlite3 connection during an error handling block. Always use try-finally blocks or context managers.
*   **Hardcoded Hostnames**: In frontends, fetch APIs using relative paths (e.g., `/api/tasks`) rather than hardcoding `http://localhost:8000/api/tasks`. This prevents broken connections if the app is hosted on a different port.
*   **Neglecting HTML/CSS details**: Creating low-fidelity text-only frontends. Ensure your UI looks stunning and feels premium, honoring modern Web Design Aesthetics.
