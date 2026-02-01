from __future__ import annotations

import sqlite3
import random
from pathlib import Path

from app import app


DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app.db"


def test_get_login_by_username() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            "SELECT id, username, password FROM logins"
        ).fetchall()

    assert rows, "No users found in DB to test against."

    user_id, username, password = random.choice(rows)
    print(f"[api] using existing user: {username}")
    print(f"[api] user_id: {user_id}")
    print(f"[api] password for {username}: {password}")

    client = app.test_client()
    print(f"[api] GET /api/login/{username}")
    response = client.get(f"/api/login/{username}")

    data = response.get_json()
    assert response.status_code == 200
    assert data["user_id"] == user_id
    assert data["username"] == username
    assert data["password"] == password


def test_get_login_by_username_not_found() -> None:
    client = app.test_client()
    print("[api] GET /api/login/username-does-not-exist-in-db")
    response = client.get("/api/login/username-does-not-exist-in-db")

    print(f"[api] status={response.status_code} body={response.get_json()}")
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}
