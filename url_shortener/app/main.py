from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import string
import secrets
from datetime import datetime, timezone

from app.database import (
    init_db,
    create_short_url,
    get_url_by_code,
    increment_clicks,
    get_all_urls,
    delete_url_by_code
)
from app.schemas import URLCreate, URLResponse

BASE62_CHARS = string.ascii_letters + string.digits
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

def generate_random_code(length: int = 6) -> str:
    """Generates a secure random 6-character Base62 string."""
    return "".join(secrets.choice(BASE62_CHARS) for _ in range(length))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup initialization."""
    init_db()
    yield

app = FastAPI(
    title="Premium URL Shortener",
    description="A micro-sized, high-performance URL shortener with analytics, TTL, and QR codes.",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static directory for JS and CSS files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    """Serves the frontpage SPA interface."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h2>index.html not found</h2>", status_code=404)
    return FileResponse(index_path)

@app.post("/api/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreate, request: Request):
    """Creates a shortened URL with optional custom alias and expiration."""
    # Handle custom alias
    if payload.custom_alias:
        existing = get_url_by_code(payload.custom_alias)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The alias '{payload.custom_alias}' is already in use. Please choose another one."
            )
        short_code = payload.custom_alias
    else:
        # Loop until we find a non-colliding random code
        for _ in range(10):
            short_code = generate_random_code()
            if not get_url_by_code(short_code):
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not generate a unique short code. Please try again."
            )

    # Handle expiration calculation
    expires_at = None
    if payload.expires_in_minutes:
        from datetime import timedelta
        exp_time = datetime.now(timezone.utc) + timedelta(minutes=payload.expires_in_minutes)
        expires_at = exp_time.isoformat()

    # Save to SQLite
    record = create_short_url(
        short_code=short_code,
        original_url=payload.original_url,
        expires_at=expires_at
    )

    # Construct complete short url link
    base_url = str(request.base_url)
    record["short_url"] = f"{base_url}{short_code}"

    return record

@app.get("/api/urls", response_model=list[URLResponse])
def list_urls(request: Request):
    """Retrieves all shortened URLs for the dashboard view."""
    records = get_all_urls()
    base_url = str(request.base_url)
    for r in records:
        r["short_url"] = f"{base_url}{r['short_code']}"
    return records

@app.get("/api/stats/{short_code}", response_model=URLResponse)
def get_stats(short_code: str, request: Request):
    """Fetches stats for a specific short code."""
    record = get_url_by_code(short_code)
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found.")
    record["short_url"] = f"{str(request.base_url)}{short_code}"
    return record

@app.delete("/api/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(short_code: str):
    """Deletes/revokes a shortened URL."""
    success = delete_url_by_code(short_code)
    if not success:
        raise HTTPException(status_code=404, detail="Short URL not found.")
    return None

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    """Redirects visitors to the original URL if valid and active."""
    # Filter out standard asset files like favicon
    if short_code in ("favicon.ico", "robots.txt"):
        raise HTTPException(status_code=404)

    record = get_url_by_code(short_code)
    if not record:
        # Return a premium HTML 404 Error page instead of plain JSON
        return HTMLResponse(
            content=get_error_page_html("Link Not Found", "The shortened URL you are looking for does not exist in our system."),
            status_code=404
        )

    # Validate Expiration
    if record["expires_at"]:
        expires_dt = datetime.fromisoformat(record["expires_at"])
        if datetime.now(timezone.utc) > expires_dt:
            return HTMLResponse(
                content=get_error_page_html("Link Expired", "The lifespan of this shortened URL has ended and it is no longer active."),
                status_code=410
            )

    # Track Click Redirect
    increment_clicks(short_code)

    return RedirectResponse(url=record["original_url"])

def get_error_page_html(title: str, message: str) -> str:
    """Returns a highly polished modern dark-mode error page."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | Shortener</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #0b0f19;
                --text: #f3f4f6;
                --accent: #ef4444;
                --card-bg: rgba(255, 255, 255, 0.03);
                --card-border: rgba(255, 255, 255, 0.08);
            }}
            body {{
                margin: 0;
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg);
                color: var(--text);
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                overflow: hidden;
            }}
            .bg-glow {{
                position: absolute;
                width: 300px;
                height: 300px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(239, 68, 68, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
                filter: blur(50px);
                z-index: -1;
            }}
            .card {{
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid var(--card-border);
                border-radius: 24px;
                padding: 3rem 2rem;
                max-width: 450px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }}
            .icon {{
                font-size: 4rem;
                margin-bottom: 1.5rem;
                display: inline-block;
                animation: float 4s ease-in-out infinite;
            }}
            h1 {{
                font-size: 2rem;
                font-weight: 800;
                margin: 0 0 1rem;
                background: linear-gradient(135deg, #ff8a8a, var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            p {{
                font-size: 1.1rem;
                color: #9ca3af;
                line-height: 1.6;
                margin: 0 0 2rem;
            }}
            .btn {{
                display: inline-block;
                background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
                border: 1px solid var(--card-border);
                color: var(--text);
                padding: 0.8rem 2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            .btn:hover {{
                background: var(--text);
                color: var(--bg);
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(255, 255, 255, 0.15);
            }}
            @keyframes float {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
        </style>
    </head>
    <body>
        <div class="bg-glow"></div>
        <div class="card">
            <span class="icon">⚠️</span>
            <h1>{title}</h1>
            <p>{message}</p>
            <a href="/" class="btn">Back to Dashboard</a>
        </div>
    </body>
    </html>
    """
