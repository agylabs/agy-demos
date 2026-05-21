from pydantic import BaseModel, Field, field_validator
from typing import Optional
from urllib.parse import urlparse

class URLCreate(BaseModel):
    original_url: str = Field(..., description="The original long URL to shorten")
    custom_alias: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_-]+$", description="An optional custom short code alias")
    expires_in_minutes: Optional[int] = Field(None, gt=0, description="Optional lifespan of the shortened URL in minutes")

    @field_validator("original_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        parsed = urlparse(value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("The provided URL is invalid. It must contain a scheme (http or https) and a domain.")
        if parsed.scheme not in ("http", "https"):
            raise ValueError("The URL scheme must be http or https.")
        return value

class URLResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: str
    expires_at: Optional[str] = None
    clicks: int
    last_clicked_at: Optional[str] = None
