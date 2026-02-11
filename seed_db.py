import os
import secrets
import sqlite3
import string
from typing import Iterable, List, Tuple

DB_PATH = os.getenv("DB_PATH", "data/app.db")

ALLOWED_CHARS = string.ascii_letters + string.digits
BAD_CHARS = "!@#$%^&*()"


def _rand_str(length: int = 8) -> str:
    return "".join(secrets.choice(ALLOWED_CHARS) for _ in range(length))


def _rand_with_bad_char(length: int = 7) -> str:
    return _rand_str(length) + secrets.choice(BAD_CHARS)


def _ensure_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()


def _build_seed_users(include_aa: bool) -> List[Tuple[str, str]]:
    dup_user = _rand_str()
    dup_pass = _rand_str()
    seed_users = [
        (_rand_str(), _rand_str()),
        (_rand_str(), _rand_str()),
        (_rand_str(), _rand_str()),
        (_rand_str(), _rand_str()),
        (_rand_with_bad_char(), _rand_with_bad_char()),  # forbidden char in username + password
        (dup_user, dup_pass),
        (dup_user, dup_pass),  # duplicate row
        ("", _rand_str()),  # empty username
        (_rand_str(), ""),  # empty password
    ]
    if include_aa:
        seed_users.append(("AA", "AA"))
    return seed_users


def seed_db(db_path: str | None = None, include_aa: bool = False) -> List[Tuple[str, str]]:
    path = db_path or DB_PATH
    seed_users = _build_seed_users(include_aa)

    with sqlite3.connect(path) as connection:
        _ensure_table(connection)
        connection.executemany(
            "INSERT INTO logins (username, password) VALUES (?, ?)",
            seed_users,
        )
        connection.commit()

    return seed_users


def _print_seed(seed_users: Iterable[Tuple[str, str]]) -> None:
    seed_list = list(seed_users)
    print("Seed data added:", len(seed_list), "rows")
    for user in seed_list:
        print(user)


if __name__ == "__main__":
    users = seed_db()
    _print_seed(users)
