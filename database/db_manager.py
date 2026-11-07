
import sqlite3
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT NOT NULL,
                agent_response TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Safely add evaluation column to existing databases
        cursor.execute("PRAGMA table_info(workflow_history)")
        columns = [row["name"] for row in cursor.fetchall()]

        if "evaluation" not in columns:
            cursor.execute("""
                ALTER TABLE workflow_history
                ADD COLUMN evaluation TEXT
            """)

    print("Database initialized successfully!")


def save_document(filename):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO documents (filename) VALUES (?)",
            (filename,)
        )
        return cursor.lastrowid


def save_workflow(query, response, status="Completed", evaluation=None):
    evaluation_json = (
        json.dumps(evaluation)
        if evaluation is not None
        else None
    )

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO workflow_history
            (user_query, agent_response, status, evaluation)
            VALUES (?, ?, ?, ?)
        """, (query, response, status, evaluation_json))

        return cursor.lastrowid


def get_workflow_history(limit=10):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, user_query, agent_response,
                   status, created_at, evaluation
            FROM workflow_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        return [dict(row) for row in cursor.fetchall()]


def get_documents():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, filename, uploaded_at
            FROM documents
            ORDER BY id DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


if __name__ == "__main__":
    initialize_database()
