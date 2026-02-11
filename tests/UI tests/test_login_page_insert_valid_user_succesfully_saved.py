from __future__ import annotations

import os
import re
import sqlite3
import uuid
from pathlib import Path

from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app.db"


def test_login_inserts_user(page: Page) -> None:
    # Arrange
    username = "XX"
    password = "YY"

    # Act
    page.goto(f"{BASE_URL}/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.wait_for_timeout(5000)
    page.click('button[type="submit"]')
    page.wait_for_timeout(5000)

    # Assert
    expect(page).to_have_url(re.compile(r"/success"))
    expect(page.locator("h1")).to_have_text("Saved!")
    expect(page.locator("strong")).to_have_text(username)

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM logins WHERE username = ? AND password = ?",
            (username, password),
        )
        assert cursor.fetchone()[0] > 0
