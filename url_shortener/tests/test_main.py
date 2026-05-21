import unittest
import sys
import os
from datetime import datetime, timedelta, timezone

# Dynamically add the url_shortener folder to sys.path so we can import 'app' modules cleanly
SYS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_DIR not in sys.path:
    sys.path.append(SYS_DIR)

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, init_db

class TestURLShortener(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in this class."""
        # Initialize test database tables
        init_db()

    def setUp(self):
        """Runs before each individual test case to reset the database."""
        self.client = TestClient(app)
        # Clear out any existing records to keep tests deterministic
        with get_db() as conn:
            conn.execute("DELETE FROM urls")
            conn.commit()

    def test_create_short_url_success(self):
        response = self.client.post(
            "/api/shorten",
            json={"original_url": "https://www.google.com"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("short_code", data)
        self.assertEqual(data["original_url"], "https://www.google.com")
        self.assertIn("short_url", data)
        self.assertEqual(data["clicks"], 0)

    def test_invalid_url_format(self):
        # Invalid URL schema or lack of domain should fail validation
        response = self.client.post(
            "/api/shorten",
            json={"original_url": "invalid-url-no-schema"}
        )
        self.assertEqual(response.status_code, 422) # Unprocessable Entity

    def test_unsupported_scheme(self):
        # ftp scheme is not allowed
        response = self.client.post(
            "/api/shorten",
            json={"original_url": "ftp://files.example.com"}
        )
        self.assertEqual(response.status_code, 422)

    def test_custom_alias_success(self):
        response = self.client.post(
            "/api/shorten",
            json={
                "original_url": "https://github.com",
                "custom_alias": "my-github-link"
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["short_code"], "my-github-link")

    def test_duplicate_custom_alias_fails(self):
        # Create first
        self.client.post(
            "/api/shorten",
            json={"original_url": "https://github.com", "custom_alias": "promo"}
        )
        # Try creating second with same alias
        response = self.client.post(
            "/api/shorten",
            json={"original_url": "https://gitlab.com", "custom_alias": "promo"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("already in use", response.json()["detail"])

    def test_redirection_and_click_tracking(self):
        # 1. Create short URL
        create_res = self.client.post(
            "/api/shorten",
            json={"original_url": "https://news.ycombinator.com"}
        )
        short_code = create_res.json()["short_code"]

        # 2. Call redirection and verify redirect status
        # Note: follow_redirects=False to verify the 307 response code
        redirect_res = self.client.get(f"/{short_code}", follow_redirects=False)
        self.assertEqual(redirect_res.status_code, 307)
        self.assertEqual(redirect_res.headers["location"], "https://news.ycombinator.com")

        # 3. Check stats to ensure clicks incremented
        stats_res = self.client.get(f"/api/stats/{short_code}")
        self.assertEqual(stats_res.status_code, 200)
        stats_data = stats_res.json()
        self.assertEqual(stats_data["clicks"], 1)
        self.assertIsNotNone(stats_data["last_clicked_at"])

    def test_expired_link_returns_410(self):
        # Create a short link set to expire in 1 minute
        create_res = self.client.post(
            "/api/shorten",
            json={
                "original_url": "https://example.com",
                "expires_in_minutes": 1
            }
        )
        short_code = create_res.json()["short_code"]

        # Directly manipulate the SQLite DB to set expires_at in the past
        past_time = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        with get_db() as conn:
            conn.execute("UPDATE urls SET expires_at = ? WHERE short_code = ?", (past_time, short_code))
            conn.commit()

        # Try to redirect and verify it returns a 410 (Gone) HTML response
        redirect_res = self.client.get(f"/{short_code}")
        self.assertEqual(redirect_res.status_code, 410)
        self.assertIn("Link Expired", redirect_res.text)

    def test_delete_url(self):
        create_res = self.client.post(
            "/api/shorten",
            json={"original_url": "https://example.com"}
        )
        short_code = create_res.json()["short_code"]

        # Delete it
        del_res = self.client.delete(f"/api/urls/{short_code}")
        self.assertEqual(del_res.status_code, 204) # 204 No Content
        
        # Verify stats returns 404
        stats_res = self.client.get(f"/api/stats/{short_code}")
        self.assertEqual(stats_res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
