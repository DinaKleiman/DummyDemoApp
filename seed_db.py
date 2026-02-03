import secrets
import sqlite3
import string

DB_PATH = "data/app.db"

ALLOWED_CHARS = string.ascii_letters + string.digits
BAD_CHARS = "!@#$%^&*()"


def rand_str(length: int = 8) -> str:
    return "".join(secrets.choice(ALLOWED_CHARS) for _ in range(length))


def rand_with_bad_char(length: int = 7) -> str:
    return rand_str(length) + secrets.choice(BAD_CHARS)


dup_user = rand_str()
dup_pass = rand_str()

seed_users = [
    (rand_str(), rand_str()),
    (rand_str(), rand_str()),
    (rand_str(), rand_str()),
    (rand_str(), rand_str()),
    (rand_with_bad_char(), rand_with_bad_char()),  # forbidden char in username + password
    (dup_user, dup_pass),
    (dup_user, dup_pass),  # duplicate row
    ("", rand_str()),  # empty username
    (rand_str(), ""),  # empty password
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executemany(
    "INSERT INTO logins (username, password) VALUES (?, ?)",
    seed_users,
)

conn.commit()
conn.close()

print("Seed data added:", len(seed_users), "rows")
for user in seed_users:
    print(user)
