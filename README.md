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

## Notes

This app is intentionally simple for local testing. Do not use it as-is for production authentication.
