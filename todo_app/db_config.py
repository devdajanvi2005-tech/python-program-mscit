import sqlite3

DATABASE = "todo.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            is_completed BOOLEAN NOT NULL DEFAULT 0,
            due_date DATE NOT NULL
        )
    """)

    conn.commit()
    conn.close()