from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, Response, jsonify, redirect, render_template, request, url_for

INVALID_USERNAME_CHARS = set("!@#$%^&*()")

def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
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


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "app.db"

app = Flask(__name__)
init_db()


@app.route("/", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if any(char in INVALID_USERNAME_CHARS for char in username):
            return render_template(
                "login.html",
                username_error="!@#$%^&*() symbols are not allowed",
                username=username,
            )
        if username and password:
            with sqlite3.connect(DB_PATH) as connection:
                connection.execute(
                    "INSERT INTO logins (username, password) VALUES (?, ?)",
                    (username, password),
                )
                connection.commit()
            return redirect(url_for("success", username=username))
        return render_template(
            "login.html",
            error="Please enter both a username and password.",
            username=username,
        )

    return render_template("login.html")


@app.route("/api/login/<username>")
def get_login(username: str):
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute(
            "SELECT id, username, password FROM logins WHERE username = ? ORDER BY id DESC LIMIT 1",
            (username,),
        ).fetchone()
    if row is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user_id": row[0], "username": row[1], "password": row[2]})


@app.route("/openapi.json")
def openapi_spec() -> Response:
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "Dummy Demo App API", "version": "1.0.0"},
        "paths": {
            "/api/login/{username}": {
                "get": {
                    "summary": "Get login by username",
                    "parameters": [
                        {
                            "name": "username",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Login found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "user_id": {"type": "integer"},
                                            "username": {"type": "string"},
                                            "password": {"type": "string"},
                                        },
                                        "required": ["user_id", "username", "password"],
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "User not found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"error": {"type": "string"}},
                                        "required": ["error"],
                                    }
                                }
                            },
                        },
                    },
                }
            }
        },
    }
    return jsonify(spec)


@app.route("/api/docs")
def swagger_ui() -> Response:
    html = """
<!doctype html>
<html>
  <head>
    <title>API Docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
      });
    </script>
  </body>
</html>
"""
    return Response(html, mimetype="text/html")


@app.route("/success")
def success() -> str:
    username = request.args.get("username", "")
    return render_template("success.html", username=username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
