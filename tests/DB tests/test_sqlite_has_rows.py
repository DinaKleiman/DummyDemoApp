import os
import sqlite3
import unittest


class TestSqliteHasRows(unittest.TestCase):
    def test_sqlite_has_any_row(self):
        db_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "app.db",
        )
        db_path = os.path.abspath(db_path)
        self.assertTrue(os.path.exists(db_path), f"Database not found: {db_path}")

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='logins'"
            )
            table = cursor.fetchone()
            self.assertIsNotNone(table, "Table 'logins' not found in database")

            count = conn.execute("SELECT COUNT(1) FROM logins").fetchone()[0]
            self.assertGreater(count, 0, "No rows found in table 'logins'")
        finally:
            conn.close()

    def test_logins_row_count(self):
        db_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "app.db",
        )
        db_path = os.path.abspath(db_path)
        self.assertTrue(os.path.exists(db_path), f"Database not found: {db_path}")

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='logins'"
            )
            table = cursor.fetchone()
            self.assertIsNotNone(table, "Table 'logins' not found in database")

            count = conn.execute("SELECT COUNT(1) FROM logins").fetchone()[0]
            print(f"logins row count: {count}")
            self.assertGreaterEqual(
                count, 0, f"Row count should be non-negative (count={count})"
            )
        finally:
            conn.close()

    def test_user_aa_has_password_aa(self):
        db_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "app.db",
        )
        db_path = os.path.abspath(db_path)
        self.assertTrue(os.path.exists(db_path), f"Database not found: {db_path}")

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='logins'"
            )
            table = cursor.fetchone()
            self.assertIsNotNone(table, "Table 'logins' not found in database")

            count = conn.execute(
                "SELECT COUNT(1) FROM logins WHERE username = ? AND password = ?",
                ("AA", "AA"),
            ).fetchone()[0]
            passwords = [
                row[0]
                for row in conn.execute(
                    "SELECT password FROM logins WHERE username = ?",
                    ("AA",),
                ).fetchall()
            ]
            self.assertGreater(
                count,
                0,
                (
                    "Expected at least 1 row for username='AA' and password='AA', "
                    f"got {count}. Passwords for 'AA' in DB: {passwords}"
                ),
            )
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
