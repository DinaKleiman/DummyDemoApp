import os
import tempfile

from seed_db import seed_db

DB_PATH = os.getenv("DB_PATH", "data/app.db")

def _seed_test_db() -> None:
    seed_db(include_aa=True)

def _cleanup_db() -> None:
    import sqlite3

    if not os.path.exists(DB_PATH):
        return
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("DELETE FROM logins")
        connection.commit()

# Ensure DB is seeded before any tests run
def pytest_sessionstart(session):
    _seed_test_db()

# Cleanup after all tests have run
def pytest_sessionfinish(session, exitstatus):
    _cleanup_db()
