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


5. Start the app:

   ```bash
   python app.py
   ```

6. Open your browser to `http://localhost:5000`.

## Data storage

Login records are stored in `data/app.db` (SQLite). Delete the file if you want to reset the data.

## Test suites


## UI tests

- `tests/test_login_playwright.py`: Playwright E2E login tests that submit credentials, confirm the success page, and verify the DB insert.
- `tests/test_login_abcd_playwright.py`: Playwright E2E test that inserts the `ABCD/ABCD` login and asserts it is saved in SQLite.

## DB tests
- `tests/DB tests/test_sqlite_has_rows.py`: Unit tests that validate the `logins` table exists and has rows (including an `AA/AA` record).

# API tests


## Notes

This app is intentionally simple for local testing. Do not use it as-is for production authentication.
