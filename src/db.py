import sqlite3
from datetime import datetime

import bcrypt

DB_PATH = "users.db"


def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT DEFAULT 'Patient'
            );
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                symptoms TEXT,
                analysis TEXT,
                timestamp TEXT
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                specialist TEXT,
                date TEXT,
                time TEXT,
                hospital TEXT
            );
        """)


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def authenticate_user(username: str, password: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        ).fetchone()
    return bool(row) and _verify(password, row[0])


def add_user(username: str, password: str) -> bool:
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, _hash(password)),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def save_history(username: str, symptoms: str, analysis: str) -> None:
    status = "Analysis Completed" if analysis.strip() else "Analysis Not Completed"
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO history (username, symptoms, analysis, timestamp) VALUES (?, ?, ?, ?)",
            (username, symptoms, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def fetch_history(username: str) -> list[tuple]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT symptoms, analysis, timestamp FROM history "
            "WHERE username = ? ORDER BY timestamp DESC",
            (username,),
        ).fetchall()


def save_appointment(
    username: str, specialist: str, date: str, time: str, hospital: str
) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO appointments (username, specialist, date, time, hospital) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, specialist, date, time, hospital),
        )
