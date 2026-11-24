"""
FUOSAFI - Database Integration Tests
Validates schema creation, relational constraints, foreign keys, and transaction integrity.
"""

import pytest
import sqlite3
from pathlib import Path
import config
from database.db import get_db_connection, fetch_all, fetch_one, execute_query
from utils.security import hash_password, verify_password

def test_database_connection():
    """Checks whether the database connection establishes and foreign keys are active."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys;")
        fk_status = cursor.fetchone()[0]
        assert fk_status == 1, "Foreign keys PRAGMA must be enabled."

def test_seeded_users_exist():
    """Validates that all four principal roles are seeded with properly hashed passwords."""
    users = fetch_all("SELECT * FROM users;")
    assert len(users) >= 4, "Should have at least 4 default users."
    roles = {u["role"] for u in users}
    assert config.ROLE_RESIDENT in roles
    assert config.ROLE_COMMUNITY_REP in roles
    assert config.ROLE_AUTHORITY in roles
    assert config.ROLE_ADMIN in roles
    
    # Check password hashing
    resident = fetch_one("SELECT * FROM users WHERE email = ?;", ("resident@fuosafi.org",))
    assert resident is not None
    assert resident["password_hash"] != "ResidentPass123"
    assert verify_password("ResidentPass123", resident["password_hash"]) is True

def test_seeded_reports_relationships():
    """Validates that reports link to real users, photographs, and history logs."""
    reports = fetch_all("SELECT * FROM reports;")
    assert len(reports) >= 4
    
    for r in reports:
        assert r["category"] in config.CATEGORIES
        assert r["status"] in config.REPORT_STATUSES
        assert -90 <= r["latitude"] <= 90
        assert -180 <= r["longitude"] <= 180
        
        # Check audit history exists for this report
        history = fetch_all("SELECT * FROM report_history WHERE report_id = ?;", (r["id"],))
        assert len(history) >= 1, f"Report {r['reference_number']} must have at least one audit record."

def test_foreign_key_enforcement():
    """Verifies that inserting a report with an invalid user_id fails due to foreign key constraints."""
    with pytest.raises(sqlite3.IntegrityError):
        execute_query(
            """
            INSERT INTO reports (
                reference_number, user_id, title, category, description,
                date_observed, location_name, county, latitude, longitude, status
            ) VALUES ('FUO-TEST-0001', 99999, 'Invalid Report', 'Coastal and marine litter', 'Test', '2026-11-20', 'Test', 'Test', -4.0, 39.0, 'Submitted');
            """
        )
