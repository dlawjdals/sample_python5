import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_FILE = Path("secure_users.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create tables and seed data if needed.

    Unlike the intentionally vulnerable demo DB, this DB is not deleted on startup.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                credit_card_number TEXT NOT NULL
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM users")
        (count,) = cursor.fetchone() or (0,)
        if count == 0:
            cursor.executemany(
                "INSERT INTO users (username, email, credit_card_number) VALUES (?, ?, ?)",
                [
                    ("hong_gildong", "hong.gildong@example.com", "0000-0000-0000-0000"),
                    ("lee_sunsin", "lee.sunsin@example.com", "9999-9999-9999-9999"),
                ],
            )

        conn.commit()


def get_user_by_username(username: str):
    """Fetch a user safely using a parameterized query."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, email, credit_card_number FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()

    if not row:
        return None

    return {"username": row[0], "email": row[1], "credit_card_number": row[2]}
