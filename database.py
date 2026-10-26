import sqlite3
from datetime import datetime

DB_NAME = "prediction_history.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # lets us access columns by name
    return conn


def init_db():
    """Create the history table if it does not exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            platform        TEXT    NOT NULL,
            release_year    INTEGER NOT NULL,
            genre           TEXT    NOT NULL,
            publisher       TEXT    NOT NULL,
            predicted_sales REAL    NOT NULL,
            created_at      TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(platform, year, genre, publisher, predicted_sales):
    """Insert one prediction record."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO prediction_history
           (platform, release_year, genre, publisher, predicted_sales, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (platform, year, genre, publisher, predicted_sales,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_all_predictions():
    """Return all records, most recent first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM prediction_history ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def delete_prediction(record_id):
    conn = get_connection()
    conn.execute("DELETE FROM prediction_history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def clear_history():
    conn = get_connection()
    conn.execute("DELETE FROM prediction_history")
    conn.commit()
    conn.close()