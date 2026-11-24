"""
FUOSAFI - Database Manager
Handles SQLite connection pooling, transactional operations, and schema initialization.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List, Dict, Any, Optional
import config


def get_db_path() -> Path:
    """Returns the database file path, ensuring parent directories exist."""
    db_path = config.DATABASE_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for SQLite connections.
    Enforces PRAGMA foreign_keys = ON, enables WAL mode, and returns dictionary-like rows.
    Automatically commits on success or rolls back on exception.
    """
    conn = sqlite3.connect(get_db_path(), timeout=30.0)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> int:
    """
    Executes an INSERT, UPDATE, or DELETE query and returns the lastrowid or affected rows.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.lastrowid


def execute_non_query(query: str, params: tuple = ()) -> int:
    """
    Executes an UPDATE or DELETE query and returns rowcount.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.rowcount


def fetch_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """
    Executes a SELECT query and returns a single row as a dictionary, or None.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None


def fetch_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Executes a SELECT query and returns all matching rows as dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def init_database(schema_path: Optional[Path] = None) -> None:
    """
    Executes the SQL schema file to initialize tables and indexes.
    """
    if schema_path is None:
        schema_path = config.BASE_DIR / "database" / "schema.sql"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_db_connection() as conn:
        conn.executescript(schema_sql)
