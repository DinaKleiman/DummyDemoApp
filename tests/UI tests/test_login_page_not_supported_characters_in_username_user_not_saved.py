from __future__ import annotations

import os
import re
import sqlite3
import uuid
from pathlib import Path

from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app.db"


def test_login_rejects_invalid_username_symbols(page: Page) -> None:
    username = f"bad!{uuid.uuid4().hex}"
    password = "Any$Pass123"

    page.goto(f"{BASE_URL}/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('.toggle-password')
    page.wait_for_timeout(3000)
    page.click('button[type="submit"]')

    expect(page).to_have_url(re.compile(r"/$"))
    expect(page.locator(".field-error")).to_have_text("!@#$%^&*() symbols are not allowed")
    expect(page.locator('input[name="username"]')).to_have_class(re.compile(r"input--error"))

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM logins WHERE username = ? AND password = ?",
            (username, password),
        )
        assert cursor.fetchone()[0] == 0
