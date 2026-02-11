# Dummy Demo App

Simple local login demo with a Flask backend and a minimal HTML/CSS UI. Submitted usernames and passwords are stored in a local SQLite database for testing purposes.

## Requirements

- Python 3.10+ (works with 3.8+)
- VS Code with the Python extension

## Run locally (VS Code)

1. Open this folder in VS Code.
2. Open a terminal in VS Code (`Terminal` → `New Terminal`).
3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
Note:   You usually only need to do this once per virtual environment, or whenever `requirements.txt` changes.

   ```bash
   pip install -r requirements.txt
   ```


5. If this is your first run (no `data/app.db` yet), seed the database:

   ```bash
   python3 seed_db.py
   ```

6. Start the app:

   ```bash
   python app.py
   ```

7. Open your browser to `http://localhost:5000`.

## Data storage

Login records are stored in `data/app.db` (SQLite). Delete the file if you want to reset the data.

## Seed script (sample data)

This project includes a seed script that inserts test users into the SQLite DB. Run it before the first app start if `data/app.db` does not exist.

- Script: `seed_db.py`
- What it does: inserts 9 rows into the `logins` table
- Each run generates **new random usernames/passwords**
- Includes special cases:
  - 1 username with a forbidden character (`!@#$%^&*()`)
  - 1 password with a forbidden character
  - 2 duplicate rows (same username + password)
  - 1 empty username
  - 1 empty password

Run it:

```bash
python3 seed_db.py
```

Note: Running the script multiple times will add more rows each time.

## Migrations

Schema changes should go into the `migrations/` folder as SQL files (for example: `001_create_tables.sql`).
This keeps the database structure in version control without committing the DB file itself.

## Test suites

Run all tests:

```bash
python3 -m pytest -q
```

Run only API + DB tests (skip UI/Playwright):

```bash
python3 -m pytest -q tests/api "tests/DB tests"
```

## UI tests

- `tests/test_login_playwright.py`: Playwright E2E login tests that submit credentials, confirm the success page, and verify the DB insert.
- `tests/test_login_abcd_playwright.py`: Playwright E2E test that inserts the `ABCD/ABCD` login and asserts it is saved in SQLite.

## DB tests
- `tests/DB tests/test_sqlite_has_rows.py`: Unit tests that validate the `logins` table exists and has rows (including an `AA/AA` record).

# API tests


## Notes

This app is intentionally simple for local testing. Do not use it as-is for production authentication.
