import sqlite3
import os
from datetime import datetime, timezone

# Resolve database file path relative to this file
DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, "shortener.db")

def get_db():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database tables."""
    os.makedirs(DB_DIR, exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                short_code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT,
                clicks INTEGER DEFAULT 0,
                last_clicked_at TEXT
            )
        """)
        conn.commit()

def create_short_url(short_code: str, original_url: str, expires_at: str = None) -> dict:
    """Inserts a new short URL record into the database."""
    created_at = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO urls (short_code, original_url, created_at, expires_at, clicks, last_clicked_at)
            VALUES (?, ?, ?, ?, 0, NULL)
            """,
            (short_code, original_url, created_at, expires_at)
        )
        conn.commit()
    return {
        "short_code": short_code,
        "original_url": original_url,
        "created_at": created_at,
        "expires_at": expires_at,
        "clicks": 0,
        "last_clicked_at": None
    }

def get_url_by_code(short_code: str) -> dict:
    """Retrieves a URL record by its short code."""
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT short_code, original_url, created_at, expires_at, clicks, last_clicked_at FROM urls WHERE short_code = ?",
            (short_code,)
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None

def increment_clicks(short_code: str):
    """Increments the click count and updates last_clicked_at for a given short code."""
    last_clicked_at = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            """
            UPDATE urls 
            SET clicks = clicks + 1, last_clicked_at = ?
            WHERE short_code = ?
            """,
            (last_clicked_at, short_code)
        )
        conn.commit()

def delete_url_by_code(short_code: str) -> bool:
    """Deletes a short URL by its code."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
        conn.commit()
        return cursor.rowcount > 0

def get_all_urls() -> list:
    """Returns all shortened URL records, sorted by creation date descending."""
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT short_code, original_url, created_at, expires_at, clicks, last_clicked_at FROM urls ORDER BY created_at DESC"
        )
        return [dict(row) for row in cursor.fetchall()]
