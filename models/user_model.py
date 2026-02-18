import sqlite3
from config import DATABASE


def create_user(name, email, password, role):
    conn = sqlite3.connect(DATABASE)
    cur  = conn.cursor()

    # Auto-approve admin, others need approval
    approved = 1 if role == "admin" else 0

    cur.execute("""
        INSERT INTO users (name, email, password, role, approved)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, password, role, approved))

    conn.commit()
    conn.close()


def get_user(email, password):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # ✅ Makes user["id"] work
    cur  = conn.cursor()

    cur.execute("""
        SELECT id, name, email, password, role, approved
        FROM users
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cur.fetchone()
    conn.close()

    return user