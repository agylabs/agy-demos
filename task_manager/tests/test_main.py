import unittest
import os
from fastapi.testclient import TestClient

# Override DB_PATH before importing main or database
import app.database
app.database.DB_PATH = "test_tasks.db"

from app.main import app
from app.database import init_db, get_db

class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure clean state
        if os.path.exists("test_tasks.db"):
            os.remove("test_tasks.db")
        init_db()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Clean up database file
        if os.path.exists("test_tasks.db"):
            os.remove("test_tasks.db")

    def setUp(self):
        # Clean up table entries between runs
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
            conn.commit()

    def test_create_task_success(self):
        payload = {
            "title": "Buy groceries",
            "description": "Milk, eggs, and bread"
        }
        response = self.client.post("/api/tasks", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Buy groceries")
        self.assertEqual(data["description"], "Milk, eggs, and bread")
        self.assertFalse(data["is_completed"])
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_create_task_validation_error(self):
        # Empty title should fail validation
        payload = {
            "title": "",
            "description": "Invalid task"
        }
        response = self.client.post("/api/tasks", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_list_tasks(self):
        # Insert test tasks
        payload1 = {"title": "Task One", "description": "Desc One"}
        payload2 = {"title": "Task Two", "description": "Desc Two"}
        self.client.post("/api/tasks", json=payload1)
        self.client.post("/api/tasks", json=payload2)

        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        # Order is DESC (newest first)
        self.assertEqual(data[0]["title"], "Task Two")
        self.assertEqual(data[1]["title"], "Task One")

    def test_update_task_success(self):
        # Insert a task
        create_resp = self.client.post("/api/tasks", json={"title": "Original Title"})
        task_id = create_resp.json()["id"]

        # Update task title and completion status
        update_payload = {
            "title": "Updated Title",
            "is_completed": True
        }
        response = self.client.put(f"/api/tasks/{task_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated Title")
        self.assertTrue(data["is_completed"])

    def test_update_task_not_found(self):
        response = self.client.put("/api/tasks/9999", json={"title": "New Title"})
        self.assertEqual(response.status_code, 404)

    def test_delete_task_success(self):
        # Insert a task
        create_resp = self.client.post("/api/tasks", json={"title": "To Delete"})
        task_id = create_resp.json()["id"]

        # Delete the task
        response = self.client.delete(f"/api/tasks/{task_id}")
        self.assertEqual(response.status_code, 204)

        # Confirm task is deleted
        list_resp = self.client.get("/api/tasks")
        self.assertEqual(len(list_resp.json()), 0)

    def test_delete_task_not_found(self):
        response = self.client.delete("/api/tasks/9999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
