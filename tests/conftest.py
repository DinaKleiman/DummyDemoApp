from pathlib import Path

from tests.seed_db import seed_db

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "app.db"

def _seed_test_db() -> None:
    seed_db(db_path=str(DB_PATH), include_aa=True)

def _cleanup_db() -> None:
    import sqlite3

    if not DB_PATH.exists():
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
