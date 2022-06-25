import sqlite3


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('persistence.db')
    conn.row_factory = sqlite3.Row
    return conn