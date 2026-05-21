from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List

from app.database import get_db, init_db
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database table on startup
    init_db()
    yield

app = FastAPI(
    title="Task Manager API",
    description="A high-performance FastAPI + SQLite Task Manager application.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    now_str = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (title, description, is_completed, created_at, updated_at)
            VALUES (?, ?, 0, ?, ?)
            """,
            (task_in.title, task_in.description, now_str, now_str)
        )
        conn.commit()
        task_id = cursor.lastrowid
        
        # Retrieve the newly inserted task
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "is_completed": bool(row["is_completed"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

@app.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks():
    tasks = []
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        rows = cursor.fetchall()
        for row in rows:
            tasks.append({
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "is_completed": bool(row["is_completed"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
    return tasks

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Calculate update fields
        title = task_in.title if task_in.title is not None else row["title"]
        description = task_in.description if task_in.description is not None else row["description"]
        is_completed = int(task_in.is_completed) if task_in.is_completed is not None else row["is_completed"]
        now_str = datetime.now(timezone.utc).isoformat()
        
        cursor.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, is_completed = ?, updated_at = ?
            WHERE id = ?
            """,
            (title, description, is_completed, now_str, task_id)
        )
        conn.commit()
        
        # Retrieve the updated task
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        updated_row = cursor.fetchone()

    return {
        "id": updated_row["id"],
        "title": updated_row["title"],
        "description": updated_row["description"],
        "is_completed": bool(updated_row["is_completed"]),
        "created_at": updated_row["created_at"],
        "updated_at": updated_row["updated_at"]
    }

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return None

# Mount the static directory
# First ensure the directory exists
import os
os.makedirs("task_manager/app/static", exist_ok=True)
app.mount("/", StaticFiles(directory="task_manager/app/static", html=True), name="static")
